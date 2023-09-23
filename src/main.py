import argparse, openai, os
import gradio as gr
from chat_utils import ChatGPT

parser = argparse.ArgumentParser()
parser.add_argument("guidelines_file_path", help="JSON file path for guidelines")
args = parser.parse_args()

chat = ChatGPT(args.guidelines_file_path)

def predict(message, history):
    yield chat.generate_response(message)

gr.ChatInterface(predict, title="Sales Assitant backed by GPT").queue().launch(share=True)