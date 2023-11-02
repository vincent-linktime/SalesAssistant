import string, os

from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.globals import set_debug
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from vectordb import VectorDB
from graphdb import GraphDB
import prompts

set_debug(True)
MODEL_NAME = "gpt-3.5-turbo"

class ChatGPT:
    """
    A class for interacting with an AI chat model.
    """

    def __init__(self):
        """
        Initializes a ChatGPT instance.

        """
        self.messages = [] 
        self.messages.append(SystemMessage(content=prompts.LIVE_CHAT_PROMPT))
        self.ai_message = None

        graph_db = GraphDB()
        vector_db = VectorDB()
        self.cypher_chain = graph_db.get_cypher_chain()
        self.vector_chain = vector_db.get_vector_chain()
        self.init_agents()

    def init_agents(self):
        tools = [
            Tool(
                name="Vector",
                func=self.vector_chain.run,
                description="""Useful when you need to answer the general questions.
                Not useful for answering questions about the detail of KDP product.
                Use full question as input.
                """,
            ),
            Tool(
                name="Graph",
                func=self.cypher_chain.run,
                description="""Useful when you need to answer questions about the detail of KDP product,
                and its components, features, or related technologies. Also useful for any sort of 
                aggregation like counting the number of components, etc.
                Use full question as input.
                """,
            ),
        ]

        self.memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
        self.mrkl = initialize_agent(
            tools, 
            ChatOpenAI(temperature=0, model_name=MODEL_NAME),
            agent=AgentType.OPENAI_FUNCTIONS, 
            memory=self.memory,
            verbose=True,
            max_iterations=2,
            early_stopping_method="generate",
        )        

    def generate_response_for_general_questions(self, question):
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


    def find_objections_or_acceptances(self, question):
        """
        Detects whether there is an objection or acceptance.

        Parameters:
            question (str): The customer inquiry.

        Returns:
            str: The question, or None if no objection/acceptance was found.

        """
        human_message = HumanMessage(content=question)
        sys_message = SystemMessage(content=prompts.DETECT_ACCEPTANCE_OR_OBJECTION_PROMPT)
        response = self.chat([sys_message, human_message])
        return response.content

    def query_vector(self, question):
        """
        Generates a response from a customer inquiry
        Parameters:
            question (str): The question to generate a response from.

        Returns:
            str: The response generated from the inquiry.
        """
        response = self.find_objections_or_acceptances(question)
        if response[:2].translate(str.maketrans('', '', string.punctuation)).lower() == 'no':
            return self.generate_response_for_general_questions(question)
        else:
            results = self.db.query_db(response)
            sys_message = SystemMessage(content=prompts.GUIDELINES_PROMPT)
            human_message = HumanMessage(content=f'Customer objection: {response}, ||| Relevant guidelines: {results} ||| Question: {question}')
            response = self.chat([sys_message, human_message])
            self.ai_message = AIMessage(content=str(response.content))
            return response.content

    def query(self, question):
        return self.mrkl.run(question)
