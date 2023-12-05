import arxiv
from langchain.utilities.arxiv import ArxivAPIWrapper
from langchain.utilities.metaphor_search import MetaphorSearchAPIWrapper
from langchain.utilities.google_search import GoogleSearchAPIWrapper
from scholarly import scholarly
from langchain.agents import tool
from embedchain import Pipeline as App
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from tqdm import tqdm
import time
import os
from langchain.vectorstores.faiss import FAISS
from langchain.storage.file_system import LocalFileStore
from langchain.embeddings.cache import CacheBackedEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from metaphor_python import Metaphor


def construct_vectorstore():
    local_file_store = LocalFileStore("./cache/")
    embeddings = OpenAIEmbeddings()
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(embeddings, local_file_store, namespace=embeddings.model)
    loader = PyMuPDFLoader("./paper_please_docs.pdf")
    docs = loader.load_and_split()
    vectorstore = FAISS.from_documents(docs, cached_embedder)
    retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5})

    return retriever

metaphor = Metaphor(api_key=os.environ["METAPHOR_API_KEY"])
metaphor_bot = MetaphorSearchAPIWrapper(metaphor_api_key=os.environ["METAPHOR_API_KEY"])
google_bot = GoogleSearchAPIWrapper()
pdf_bot = App()
retriever = construct_vectorstore()

def store_documents(url: str):
    """ Useful for storing documents in vectorstore for next question. If you get a URL from a search, you can store it in a vectorstore."""
    progress_bar = tqdm(total=1, desc="store_documents", unit="result")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(PyMuPDFLoader(url).load())
    retriever.add_documents(texts)
    progress_bar.update(1)
    time.sleep(0.1)

    progress_bar.close()

@tool
def google_search(question: str) -> str:
    """ Google search to get the latest results. Question should be a fully formed question. """
    return google_bot.run(question)

@tool
def arxiv_search(topic: str) -> str:
    """ useful for when you need to answer questions about research paper. Topic should be a topic of research paper or name of research paper."""
    arxiv_bot = ArxivAPIWrapper(
        top_k_results = 1,
        ARXIV_MAX_QUERY_LENGTH = 300,
        load_max_docs = 100,
        load_all_available_meta = False,
        doc_content_chars_max = 10000
    )
    return arxiv_bot.run(topic)

@tool
def get_url(input: str, max_results=1) -> list:
    """ Get URL of a research paper. Useful for getting url of topic from arxiv. input should be a topic of research paper."""
    client = arxiv.Client()
    search = arxiv.Search(
        query=input,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    
    url_list = []
    for result in client.results(search):
        url_list.append(result.pdf_url)

    return url_list

toolset = [google_search, arxiv_search, get_url]


# @tool
# def search_metaphor(topic: str):
#     """ Useful for getting title or url or author or published date of topic"""
#     metaphor_bot = MetaphorSearchAPIWrapper()
    
#     return metaphor_bot.results(topic, 1)
        

# @tool
# def get_url_scholarly(topic: str):
#     """ Useful for getting url of topic from google scholar. Get URL of a research paper."""
#     output = scholarly.search_pubs(topic)
#     url = [next(output, None)["eprint_url"]]
#     # store_documents(url)
    
#     return url

# @tool
# def search(query: str, include_domains=None, start_published_date=None):
#     """ useful for when you need to answer questions about latest research paper. The input should be both a topic and a fully formed question.
#     Set the optional include_domains (list[str]) parameter to restrict the search to a list of domains.
#     Set the optional start_published_date (str) parameter to restrict the search to documents published after the date (YYYY-MM-DD).
#     """
#     return metaphor_bot._metaphor_search_results(
#         f"{query}",
#         use_autoprompt=True,
#         num_results=3,
#         include_domains=include_domains,
#         start_published_date=start_published_date,
#     )




# @tool
# def get_contents(url: str):
#     """ Get summary and description of URL. Get the contents of a webpage."""
#     pdf_bot.add(url)
#     answer = pdf_bot.query("Summarize what the link is about in 5 sentences or less.")
#     return answer