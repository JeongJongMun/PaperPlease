import os
import glob
from langchain.document_loaders import PyPDFLoader

def pypaperbot(q: str):
    command = f"python -m PyPaperBot --query=\"{q}\" --scholar-pages=1 --scholar-results=1 --restrict=1 --dwn-dir=\"C:/dl/Project/paper-please/static/papers/\""
    print("Command: ", command)
    # os.system(command)
    
    output = os.popen(command).read()
    print("Output: ", output)
    
    # loader = PyPDFLoader(file_path="C:/dl/Project/paper-please/static/papers/")
    
    return q

# # 예시로 함수 호출
# query_string = 'attention is all you need'
# pypaperbot(query_string)


# ## Load Document
# pdf_files = glob.glob("*.pdf")
# pdf_file_paths = [os.path.abspath(file) for file in pdf_files]

# nested_docs = [PyPDFLoader(file_path).load() for file_path in pdf_file_paths]
# docs = [doc for sublist in nested_docs for doc in sublist]


# # 도큐먼트에 쿼리를 날릴 수 있는 방법
# # similarity_search를 함수로 래핑해서 러너블 람다에 넣으면 LCEL에서 사용 가능임
# def format_docs(docs):
#     return "\n\n".join([d.page_content for d in docs])

# def retreiver(query):
#     return db.similarity_search(query, k=5)

# chain = (
#     ("content": RunnableLambda(retreiver) | format_docs, "question": RunnablePassthrough)
#     | prompt
#     | model
#     | StrOutPutParser
# )