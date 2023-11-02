import gradio as gr
from agent import SalesAgentExecutor

agent_executor = SalesAgentExecutor().get_agent_executor()

def predict(message, history):
    yield agent_executor.run(message)

gr.ChatInterface(predict, title="Sales Assistant backed by GPT").queue().launch(share=True)