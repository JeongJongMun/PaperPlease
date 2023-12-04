import os
from langchain.utilities.metaphor_search import MetaphorSearchAPIWrapper

search = MetaphorSearchAPIWrapper(metaphor_api_key=os.environ.get("METAPHOR_API_KEY", None))

ans = search.results("Attention is all you need", 5)

print(ans)