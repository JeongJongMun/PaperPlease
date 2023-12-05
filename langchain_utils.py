from libraries import *

# Cache
langchain.llm_cache = InMemoryCache()
# Memory
memory = ConversationBufferMemory(memory_key="history", return_messages=True)
# RAG
retriever = construct_vectorstore()

# ChatModel
chat_model = ChatOpenAI(model="gpt-3.5-turbo-1106").configurable_alternatives(
    ConfigurableField(id="chatmodel"),
    default_key="gpt3.5",
    gpt4=ChatOpenAI(model="gpt-4-1106-preview"),
    cohere=ChatCohere(), 
).with_config(configurable={"chatmodel": "gpt3.5"}) # Configureable Field

# Binding Tools
llm_with_tools = chat_model.bind(
    functions=[format_tool_to_openai_function(t) for t in toolset]
)

# Check Agent intermediate steps
def pp(prompt):
    print(prompt)
    print()
    return prompt

# Chain
agent_with_memory = (RunnablePassthrough.assign(
        context=itemgetter('input') | retriever,
        chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter('history'),
        agent_scratchpad=RunnableLambda(itemgetter('intermediate_steps')) | format_to_openai_functions,
    )
    | RunnableLambda(pp)
    | chat_prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

# Agent Executor
agent_executor = AgentExecutor(memory=memory, agent=agent_with_memory, tools=toolset, verbose=False, max_iterations=3, handle_parsing_errors=True)