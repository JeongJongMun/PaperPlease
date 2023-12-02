from langchain.utilities.metaphor_search import MetaphorSearchAPIWrapper

search = MetaphorSearchAPIWrapper()

search.results("The best blog post about AI safety is definitely this: ", 10)