import argparse, openai, os
import gradio as gr
from chat_utils import ChatGPT

chat = ChatGPT()

def predict(message, history):
    yield chat.query(message)

gr.ChatInterface(predict, title="Sales Assistant backed by GPT").queue().launch(share=True)