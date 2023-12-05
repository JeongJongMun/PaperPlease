from tools import toolset
import langchain
from langchain.cache import InMemoryCache
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI, ChatCohere
from langchain.schema.runnable import ConfigurableField, RunnableLambda, RunnablePassthrough
from prompt import chat_prompt
from operator import itemgetter
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor

from tools import retriever

# Cache
langchain.llm_cache = InMemoryCache()
# Memory
memory = ConversationBufferMemory(memory_key="history", return_messages=True)
# RAG

# ChatModel & ConfigurableField
chat_model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.9)

# Binding Tools
llm_with_tools = chat_model.bind(
    functions=[format_tool_to_openai_function(t) for t in toolset]
)

# print 
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
agent_executor = AgentExecutor(memory=memory, 
                               agent=agent_with_memory, 
                               tools=toolset, 
                               verbose=True,
                               max_execution_time=60,
                               max_iterations=5,
                               early_stopping_method="force").configurable_alternatives(
                                                                ConfigurableField(id="chatmodel"),
                                                                default_key="GPT3",
                                                                GPT4=ChatOpenAI(model="gpt-4-1106-preview"),
                                                                Cohere=ChatCohere(),)

def update_config(input):
    global agent_executor
    agent_executor = agent_executor.with_config(configurable={'chatmodel': input['_chatmodel']})
    
    return {"input": itemgetter("input")(input)}