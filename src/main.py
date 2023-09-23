import openai, os
import gradio as gr
from chat_utils import ChatGPT


chat = ChatGPT(need_db=True)

def predict(message, history):
    yield chat.generate_response_for_objections(message)

gr.ChatInterface(predict, title="Assitant backed by GPT").queue().launch(share=True)