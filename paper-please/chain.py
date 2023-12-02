import os
from uuid import UUID
from langchain.schema.output import ChatGenerationChunk, GenerationChunk

from metaphor_python import Metaphor
from langchain.agents import tool, tools
from typing import Any, List, Optional, Union

from langchain.chat_models import ChatOpenAI, ChatCohere, ChatOllama
from langchain.agents import OpenAIFunctionsAgent
from langchain.schema import StrOutputParser

from langchain.agents import AgentExecutor
from langchain.tools.render import format_tool_to_openai_function

import langchain
from langchain.cache import InMemoryCache

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks import get_openai_callback

from langchain.memory.buffer import ConversationBufferMemory
from prompt import final_prompt, topic_or_name_prompt

from langchain.schema.runnable import ConfigurableField, RunnableLambda, RunnablePassthrough

from arxiv_pdf import download_pdf
from pypaperbot_pdf import pypaperbot

from langchain.callbacks.base import BaseCallbackHandler

os.environ["METAPHOR_API_KEY"] = "67cc1aa8-a38c-4618-93a5-ab368f439423"

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

class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwarg) -> None:
        print(f"{token}", end="")

class PaperPlease:
    # chat = PaperPlease(llm)
    def __init__(self, llm):
        
        self.prompt = topic_or_name_prompt

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)        
        
        llm.streaming = True
        llm.callbacks = [MyCustomHandler()]
        self.llm = llm
        
        self.chain = self.prompt | self.llm
    
    # chat("~~")
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
    

# not streaming
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.5).configurable_alternatives(
    ConfigurableField(id="chatmodel"),
    default_key="gpt3.5",
    gpt4=ChatOpenAI(model="gpt-4-1106-preview", temperature=0.5),
    cohere=ChatCohere(),
)

# streaming
# llm = ChatOpenAI(model="gpt-3.5-turbo-1106", streaming=True, callback=StreamingStdOutCallbackHandler())

# llm_with_tools = llm.bind(
#     functions=[format_tool_to_openai_function(t) for t in tools]
# )


# chain = final_prompt | llm | StrOutputParser()
chain = topic_or_name_prompt | llm | StrOutputParser() | RunnableLambda(pypaperbot)

runnablebind = chain.with_config(configurable={"chatmodel": "gpt3.5"})

""" Local Test
"""

# input = "Who is the Author of GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding?"

input = "What does Attention is all you need talk about?"

# input = "Give me the three most cited recent papers in natural language processing."

# input = "Why is the field of computer vision so promising?"

# Tracking Token Usage
with get_openai_callback() as callback:
    # for c in chain.stream({"input" : input}):
    #     print(c, end="", flush=True)
    answer = runnablebind.invoke({"input" : input})
    # Print Token Usage
    print(callback)
    print()
    print(answer)