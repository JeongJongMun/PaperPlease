import arxiv
from scholarly import scholarly
from embedchain import Pipeline as App
import os
from langchain.utilities.metaphor_search import MetaphorSearchAPIWrapper
from langchain.utilities.arxiv import ArxivAPIWrapper
from langchain.agents import tool, tools

@tool
def search_arxiv(topic: str):
    """ return summary of arxiv papers """
    arxiv = ArxivAPIWrapper(
        top_k_results = 3,
        ARXIV_MAX_QUERY_LENGTH = 300,
        load_max_docs = 100,
        load_all_available_meta = False,
        doc_content_chars_max = 40000
    )
    docs = arxiv.get_summaries_as_docs(topic)
    
    summaries = []
    for doc in docs:
        summaries.append(doc.page_content)
    
    return summaries

@tool
def search_metaphor(topic: str):
    """ Call search engine with a research paper title or query."""
    search = MetaphorSearchAPIWrapper(metaphor_api_key=os.environ.get("METAPHOR_API_KEY", None))
    
    return search.results(topic, 1)
        

@tool
def get_url_arxiv(topic: str, max_results=1):
    """ return url of arxiv papers"""
    client = arxiv.Client()
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    url_list = []
    for result in client.results(search):
        url_list.append(result.pdf_url)
    
    return url_list

@tool
def get_url_scholarly(topic: str):
    """ return url of google scholar papers"""
    output = scholarly.search_pubs(topic)
    
    return [next(output, None)["eprint_url"]]


tools = [search_arxiv, search_metaphor, get_url_arxiv, get_url_scholarly]


# retrieval_paper("Attention is All You Need")

# ans = retriever.get_relevant_documents("What does Attention is all you need talk about?")
# print(ans[0])

"""
Local Test


pdf_bot = App()

desired_paper = "Attention is All You Need"
result = download_pdf(desired_paper)
print(result)

for link in result:
    print(link)
    pdf_bot.add(link + ".pdf")

answer = pdf_bot.query(f"What is {desired_paper}? Describe it simply.")
print(answer)
"""