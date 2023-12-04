from libraries import *

# Cache
langchain.llm_cache = InMemoryCache()

# Memory, Vectorstore, Retriever
memory = ConversationBufferMemory(memory_key="history", return_messages=True)
retriever = construct_vectorstore()

# Language Model
llm = ChatOpenAI(model="gpt-3.5-turbo-1106").configurable_alternatives(
    ConfigurableField(id="chatmodel"),
    default_key="gpt3.5",
    gpt4=ChatOpenAI(model="gpt-4-1106-preview"),
    cohere=ChatCohere(), 
).with_config(configurable={"chatmodel": "gpt3.5"}) # Configureable Field


llm_with_tools = llm.bind(
    functions=[format_tool_to_openai_function(t) for t in toolset]
)


def pp(prompt):
    print(prompt)
    print()
    return prompt


agent_with_memory = (
    RunnablePassthrough.assign(context=itemgetter('input')  | retriever,
        chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter('history'),
        agent_scratchpad=RunnableLambda(itemgetter('intermediate_steps')) | format_to_openai_functions,
    )
    | RunnableLambda(pp)
    | chat_prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent_with_memory, tools=toolset, verbose=True, max_iterations=3)



input = """
What does Attention is all you need talk about?
"""
# print(agent_executor.invoke({'input':input}))