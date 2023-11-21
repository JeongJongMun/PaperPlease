import os

from metaphor_python import Metaphor
from langchain.agents import tool, tools
from typing import List

from langchain.chat_models import ChatGooglePalm, ChatOpenAI
from langchain.agents import OpenAIFunctionsAgent
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate

from langchain.agents import AgentExecutor
from langchain.tools.render import format_tool_to_openai_function

import langchain
from langchain.cache import InMemoryCache

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks import get_openai_callback
from prompt import final_prompt


os.environ["METAPHOR_API_KEY"] = ""

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

# Memory Cache for save money & time
langchain.llm_cache = InMemoryCache() 

# not streaming
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.5)
# streaming
# llm = ChatOpenAI(model="gpt-3.5-turbo-1106", streaming=True, callback=StreamingStdOutCallbackHandler())

# llm_with_tools = llm.bind(
#     functions=[format_tool_to_openai_function(t) for t in tools]
# )


chain = final_prompt | llm | StrOutputParser()


""" Local Test

input = "Who is the Author of 'GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding'?"

# Tracking Token Usage
with get_openai_callback() as callback:
    # for c in chain.stream({"input" : input}):
    #     print(c, end="", flush=True)
    answer = chain.invoke({"input" : input})
    # Print Token Usage
    print(callback)
    print()
    print(answer)
    
"""