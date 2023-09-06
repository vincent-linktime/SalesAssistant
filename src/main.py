import openai
import gradio 
import os
from arango import ArangoClient

# Initialize the ArangoDB client.
client = ArangoClient("http://127.0.0.1:8529")
db = client.db('Healthcare_KG', username='root', password='')

openai.api_key = os.environ["OPENAI_KEY"]

examples = ""
with open('examples.txt', 'r') as file:
    examples = file.read()

content_hcb = f""" You are an AI system specializes in generating ArangoDB AQL queries based on example AQL queries.
Example ArangoDB AQL queries are: \n {examples} \n
You will refrain from providing explanations or additional information and solely focus on generating the ArangoDB AQL queries.
You will strictly adhere to generating ArangoDB AQL queries based on the given examples.
Do not provide any AQL queries that can't be deduced from AQL query examples. 
However, if the context of the conversation is insufficient, you will inform the user and specify the missing context.
I repeat, if the context of the conversation is insufficient please inform the user and specify the missing context.
"""

content_hlr = f""" You are an AI assistant specialized in generating text responses based on the provided information. 
Your role is to generate human-readable responses using the available information from the latest prompt. 
While providing answers, you will maintain the perspective of an AI assistant. 
It is important to note that you will not add any extra information that is not explicitly provided in the given prompt. 
You will strictly adhere to generating responses solely based on the available information. 
Once again, You will refrain from including any additional details that are not explicitly given in the prompt.
"""

def human_like_response(user_input):
    messages = [
        {"role": "system", "content": content_hlr}
    ]
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = messages,
    temperature=0.5
    )
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    return reply

# check for valid AQL query
def is_aql_query(query):
    try:
        db.aql.execute(query)  
        return True 
    except Exception:
        return False

def HealthCareChatbot(user_input):
    messages = [{"role": "system", "content": content_hcb}]
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature=0.0
    )
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    if "`" in reply:
        reply = reply.split("```")[1].strip("`")  
    
    if is_aql_query(reply):
        docs = db.aql.execute(reply)
        response = [doc for doc in docs]
        if len(response) == 0:
              message = f"Apologise to the user as you don't have an information related to this particular disease, treatments, symptoms, or medical specialty. "
              response = human_like_response(message)
        else:
            response = human_like_response(",".join(response))
    else:
        message = f"Greet the user and ask more information related to diseases, treatments, symptoms, or medical specialty."
        response = human_like_response(message)
    return response

inputs = gradio.inputs.Textbox(lines=7, label="Chat with ArangoGPT")
outputs = gradio.outputs.Textbox(label="ArangoGPT Reply")
demo = gradio.Interface(fn=HealthCareChatbot, inputs = inputs, outputs = outputs, title = "HealthCare Chatbot Backed by ArangoDB")

demo.launch(share=False)