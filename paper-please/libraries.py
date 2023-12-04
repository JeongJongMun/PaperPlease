import langchain
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI, ChatCohere
from langchain.schema import StrOutputParser
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.prompts.example_selector.semantic_similarity import SemanticSimilarityExampleSelector
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder
from tqdm import tqdm
import time
from langchain.document_loaders import PyMuPDFLoader

from langchain.storage.file_system import LocalFileStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS

from langchain.embeddings.cache import CacheBackedEmbeddings
import arxiv
from scholarly import scholarly
from embedchain import Pipeline as App
import os
from langchain.utilities.metaphor_search import MetaphorSearchAPIWrapper
from langchain.utilities.arxiv import ArxivAPIWrapper
from langchain.agents import tool, tools

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks import get_openai_callback

from langchain.schema.runnable import ConfigurableField, RunnableLambda, RunnablePassthrough, RunnableParallel

from tools import tools
from prompt import topic_or_name_prompt, retrieval_prompt, chat_prompt

from langchain.memory import ConversationBufferMemory
from operator import itemgetter
from vectorspace import construct_vectorstore, store_documents


from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
import langchain
from langchain.cache import InMemoryCache
from langchain_utils import combinded_chain, get_openai_callback

from PIL import Image
import matplotlib.pyplot as plt

import base64
import os
import fitz 
import io 