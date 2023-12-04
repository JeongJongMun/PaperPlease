# main.py
from libraries import *

def main():
    # input = "Who is the Author of GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding?"
    input = "What does Attention is all you need talk about?"
    # input = "Give me the three most cited recent papers in natural language processing."
    # input = "Why is the field of computer vision so promising?"
    
    # Cache
    langchain.llm_cache = InMemoryCache()

    
    # Tracking Token Usage
    with get_openai_callback() as callback:
        output = combinded_chain.invoke({"input": input})
        print(callback)
        print()
        print(output)
        # memory.save_context(input, {'output': output.content})

if __name__ == "__main__":
    main()
