from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re

from vectordb import VectorDB
from graphdb import GraphDB
from prompts import AGENT_PROMPT_WITH_HISTORT

MODEL_NAME = "gpt-3.5-turbo"

# Set up a prompt template
class SalesPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)    

class SalesOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

class SalesAgentExecutor():
    def __init__(self):
        graph_db = GraphDB()
        vector_db = VectorDB()
        cypher_chain = graph_db.get_cypher_chain()
        vector_chain = vector_db.get_vector_chain()
        tools = [
            Tool(
                name="Vector Search",
                func=vector_chain.run,
                description="""Useful when you need to answer the general questions.
                Not useful for answering questions about the detail of KDP product.
                Use full question as input.
                """,
            ),
            Tool(
                name="Graph Search",
                func=cypher_chain.run,
                description="""Useful when you need to answer questions about the detail of KDP product,
                and its components, features, or related technologies. Also useful for any sort of 
                aggregation like counting the number of components, etc.
                Use full question as input.
                """,
            ),
        ]
        prompt_with_history = SalesPromptTemplate(
            template=AGENT_PROMPT_WITH_HISTORT,
            tools=tools,
            input_variables=["input", "intermediate_steps", "history"]
        )   
    
        output_parser = SalesOutputParser()
        llm = OpenAI(temperature=0, model_name=MODEL_NAME)
        llm_chain = LLMChain(llm=llm, prompt=prompt_with_history)
        tool_names = [tool.name for tool in tools]
        tool_names = [tool.name for tool in tools]
        memory=ConversationBufferWindowMemory(k=2)
        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names,
        )
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True, memory=memory)

    def get_agent_executor(self):
        return self.agent_executor
