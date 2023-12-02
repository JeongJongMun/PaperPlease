import arxiv

def download_pdf(q: str):
    print("Q is: ", q)
    client = arxiv.Client()
    search = arxiv.Search(
        query=q,
        max_results=1,
        sort_by=arxiv.SortCriterion.Relevance
    )

    for result in client.results(search):
        fname = result.title + ".pdf"
        result.download_pdf(
            dirpath="C:/dl/Project/paper-please/static/papers/",
            filename=fname
        )
    return q