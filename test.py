
import openai, os

openai.api_key = os.environ["OPENAI_KEY"]
os.environ["http_proxy"]="127.0.0.1:8118"
os.environ["https_proxy"]="127.0.0.1:8118"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "assistant", "content": "This is a test!"}
    ]
)

print(response)