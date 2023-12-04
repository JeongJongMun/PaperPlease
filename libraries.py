# langchain
import langchain
# agents
from langchain.agents import tool, tools, AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser, XMLAgentOutputParser, ReActSingleInputOutputParser

# cache
from langchain.cache import InMemoryCache

# callbacks
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks import get_openai_callback

# chat_models
from langchain.chat_models import ChatOpenAI, ChatCohere

# document_loaders
from langchain.document_loaders import PyMuPDFLoader

# embeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.cache import CacheBackedEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings

# memory
from langchain.memory import ConversationBufferMemory

# storage
from langchain.storage.file_system import LocalFileStore

# schema
from langchain.schema import StrOutputParser, AgentFinish
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import ConfigurableField, RunnableLambda, RunnablePassthrough, RunnableParallel

# text
from langchain.text_splitter import CharacterTextSplitter

# tools
from langchain.tools.render import format_tool_to_openai_function

# utils & utilities
from langchain.utilities.metaphor_search import MetaphorSearchAPIWrapper
from langchain.utilities.arxiv import ArxivAPIWrapper

# vectorstores
from langchain.vectorstores.chroma import Chroma
from langchain.vectorstores.faiss import FAISS

# prompts
from langchain.prompts.example_selector.semantic_similarity import SemanticSimilarityExampleSelector
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder

# etc
from operator import itemgetter
from vectorspace import construct_vectorstore, store_documents
from embedchain import Pipeline as App

# global variables
from tools import toolset
from prompt import topic_or_name_prompt, chat_prompt
from scholarly import scholarly

# paper
import arxiv

# image
import fitz, base64
from PIL import Image
import matplotlib.pyplot as plt

# system
import os, io

# time
from tqdm import tqdm
import time