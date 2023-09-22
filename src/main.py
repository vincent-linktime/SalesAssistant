import openai, os
import gradio as gr
from chat_utils import ChatGPT


chat = ChatGPT(need_db=True)

def predict(message, history):
    response = chat.generate_response_for_objections(message)

    partial_message = ""
    for chunk in response:
        if len(chunk['choices'][0]['delta']) != 0:
            partial_message = partial_message + chunk['choices'][0]['delta']['content']
            yield partial_message

gr.ChatInterface(predict, title="Assitant backed by GPT").queue().launch(share=True)