from libraries import *

@tool
def summary_arxiv(topic: str):
    """ Useful for getting a summary of a topic from arxiv """
    arxiv = ArxivAPIWrapper(
        top_k_results = 1,
        ARXIV_MAX_QUERY_LENGTH = 300,
        load_max_docs = 100,
        load_all_available_meta = False,
        doc_content_chars_max = 10000
    )
    return arxiv.get_summaries_as_docs(topic)
    

@tool
def search_metaphor(topic: str):
    """ Useful for getting title or url or author or published date of topic"""
    search = MetaphorSearchAPIWrapper(metaphor_api_key=os.environ.get("METAPHOR_API_KEY", None))
    
    return search.results(topic, 1)
        

@tool
def get_url_arxiv(topic: str, max_results=1):
    """ Useful for getting pdf url of topic from arxiv"""
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
    """ Useful for getting pdf url of topic from google scholar"""
    output = scholarly.search_pubs(topic)
    
    return [next(output, None)["eprint_url"]]

@tool
def summary_url(url: str):
    """ Useful when you have a URL and need a summary and description of that URL."""
    pdf_bot = App()
    pdf_bot.add(url)
    answer = pdf_bot.query("Describe and summarize what the link is about in 7 sentences or less.")
    return answer


tools = [summary_arxiv, search_metaphor, get_url_arxiv, get_url_scholarly, summary_url]



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