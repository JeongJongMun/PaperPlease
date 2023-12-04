from tqdm import tqdm
import time
from langchain.document_loaders import PyMuPDFLoader

from langchain.storage.file_system import LocalFileStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS

from langchain.embeddings.cache import CacheBackedEmbeddings


"""_summary_ = "PDF Loader & Vectorstore & Retrieval"
"""

def construct_vectorstore():
    local_file_store = LocalFileStore("./cache/")
    embeddings = OpenAIEmbeddings()
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(embeddings, local_file_store, namespace=embeddings.model)
    vectorstore = FAISS.from_texts([""], cached_embedder)
    retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5})

    return retriever



desired_paper = "Attention is All You Need"


def store_documents(urls, retriever):

    # Create a tqdm progress bar with the total number of iterations
    progress_bar = tqdm(total=len(urls), desc="store_documents", unit="result")
    
    for url in urls:
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(PyMuPDFLoader(url).load())
        retriever.add_documents(texts)
        # Update the progress bar
        progress_bar.update(1)
        # Simulate some processing time (you can remove this line in a real application)
        time.sleep(0.1)

    # Close the progress bar
    progress_bar.close()




