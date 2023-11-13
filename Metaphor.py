import os

from metaphor_python import Metaphor
from langchain.agents import tool, tools
from typing import List

from langchain.chat_models import ChatOpenAI
from langchain.agents import OpenAIFunctionsAgent
from langchain.schema import SystemMessage

from langchain.agents import AgentExecutor

os.environ["METAPHOR_API_KEY"] = "befbca3e-b99c-469a-a3ed-9fbebb5d4bb2"

client = Metaphor(api_key=os.environ["METAPHOR_API_KEY"])

@tool
def search(query: str):
    """Call search engine with a research paper title or query.
    you must get from arxiv"""
    return client.search(query, use_autoprompt=True, num_results=1)


@tool
def get_contents(ids: List[str]):
    """Get contents of a webpage.

    The ids passed in should be a list of ids as fetched from `search`.
    """
    return client.get_contents(ids)


@tool
def find_similar(url: str):
    """Get search results similar to a given URL.

    The url passed in should be a URL returned from `search`
    """
    return client.find_similar(url, num_results=1)

tools = [search, get_contents, find_similar]

llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0, openai_api_key="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")

system_message = SystemMessage(
    content="You are a AI Developer who uses search engines to look up information."
)
prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)
agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
