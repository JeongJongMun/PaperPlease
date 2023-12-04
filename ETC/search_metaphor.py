import os
from embedchain import Pipeline as App
from metaphor_python import Metaphor

exclude_links = ["youtube.com", "twitter.com", "facebook.com", "instagram.com", "reddit.com"]
include_links = ["scholar.google.com", "ieeexplore.ieee.org", "dl.acm.org", "arxiv.org"]
include_links = ["ieeexplore.ieee.org"]


def download_pdf(q: str):
    print(q)
    client = Metaphor(api_key=os.environ.get("METAPHOR_API_KEY", None))
    search = client.search(
        query=q,
        num_results=1,
        include_domains=include_links,
    )
    return search

# Local Test
pdf_bot = App()

# desired_paper = "Attention is All You Need"
desired_paper = "Generative Pre-trained Transformer"
result = download_pdf(desired_paper)
print(result)


# for link in result:
#     print(link)
#     pdf_bot.add(link + ".pdf")

# answer = pdf_bot.query(f"What is {desired_paper}? Describe it simply.")
# print(answer)