from setup import toolset, retriever, prompt_chat
from operator import itemgetter
import langchain
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.cache import InMemoryCache
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.tools.render import render_text_description

# chat_model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.9)


# print 
def pp(p):
    print(p)
    print()
    return p

def tt(t):
    print(type(t))
    print()
    return t

langchain.llm_cache = InMemoryCache()

memory = ConversationBufferMemory(memory_key="history", return_messages=True)

chat_model = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.2)

llm_with_stop = chat_model.bind(stop=["\nObservation"])

# Chain
chain = ( RunnableLambda(pp) | RunnablePassthrough.assign(
        input=itemgetter("input"),
        context=RunnableLambda(lambda x: retriever.get_relevant_documents(x["input"])),
        chat_history=RunnableLambda(lambda x: memory.load_memory_variables(x["input"])["history"]),
        tools=RunnableLambda(lambda x: render_text_description(toolset)),
        tool_names=RunnableLambda(lambda x: ", ".join([t.name for t in toolset])),
        agent_scratchpad=RunnableLambda(lambda x: format_log_to_str(x["intermediate_steps"])),
    )
    | prompt_chat
    | llm_with_stop
    | ReActSingleInputOutputParser()
)

# AgentExecutor
agent_executor = AgentExecutor(agent=chain, 
                                tools=toolset, 
                                verbose=True,
                                memory=memory,                                 
                                max_execution_time=60,
                                max_iterations=5,
                                handle_parsing_errors=True,                                
                                early_stopping_method="generate")