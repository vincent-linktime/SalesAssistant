import string

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from vectordb import VectorDB
import prompts


class ChatGPT:
    """
    A class for interacting with an AI chat model, querying transcripts, finding objections in transcripts
    and generating responses from sales calls.
    """

    def __init__(self, need_db=False):
        """
        Initializes a ChatGPT instance.

        """
        self.messages = []
        self.chat = ChatOpenAI(model_name="gpt-3.5-turbo")

        if need_db:
            self.db = VectorDB('data/guidelines.json')

        self.messages.append(SystemMessage(content=prompts.LIVE_CHAT_PROMPT))

        self.ai_message = None

    def generate_response(self, question):
        """
        Sends a message to the chatbot, and returns the response.

        Parameters:
            question (str): The question of the conversation.

        Returns:
            str: The response from the chatgpt.

        """
        human_message = HumanMessage(content=f'question: {question}')
        temp_messages = self.messages.copy()
        temp_messages.append(human_message)
        response = self.chat(temp_messages)
        self.messages.append(human_message)
        ai_message = AIMessage(content=response.content)
        self.messages.append(ai_message)

        return str(response.content)


    def find_objections(self, question):
        """
        Detects whether there is an objection in a transcript, and returns the objection if there is one.

        Parameters:
            transcript (str): The transcript to search for an objection in.

        Returns:
            str: The objection found in the transcript, or None if no objection was found.

        """
        human_message = HumanMessage(content=question)
        sys_message = SystemMessage(content=prompts.DETECT_OBJECTION_PROMPT)
        response = self.chat([sys_message, human_message])
        return response.content

    def generate_response_for_objections(self, question):
        """
        Generates a response from a sales call transcript if there is an objection. Queries a Deep Lake DB for relevant guidelines.

        Parameters:
            transcript (str): The transcript to generate a response from.

        Returns:
            str: The response generated from the transcript, or None if no objection was found.
        """
        response = self.find_objections(question)
        if response[:2].translate(str.maketrans('', '', string.punctuation)).lower() == 'no':
            return self.generate_response(question)
        else:
            results = self.db.query_db(response)
            sys_message = SystemMessage(content=prompts.OBJECTION_GUIDELINES_PROMPT)
            human_message = HumanMessage(content=f'Customer objection: {response}, ||| Relevant guidelines: {results} ||| Question: {question}')
            response = self.chat([sys_message, human_message])
            self.ai_message = AIMessage(content=str(response.content))
            return response.content
