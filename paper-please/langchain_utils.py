# langchain_utils.py

from langchain.chat_models import ChatOpenAI, ChatCohere
from langchain.schema import StrOutputParser


from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks import get_openai_callback

from langchain.schema.runnable import ConfigurableField, RunnableLambda, RunnablePassthrough, RunnableParallel

from tools import tools
from prompt import topic_or_name_prompt, retrieval_prompt, chat_prompt

from langchain.memory import ConversationBufferMemory
from operator import itemgetter
from vectorspace import construct_vectorstore, store_documents


from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor

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
    functions=[format_tool_to_openai_function(t) for t in tools]
)


def pp(prompt):
    print(prompt)
    return prompt


# Chain
# chain = (RunnablePassthrough.assign(context=itemgetter('input') | retriever,
#                                     chat_history=RunnableLambda(memory.load_memory_variables)| itemgetter('history')) 
#         | RunnableLambda(pp) | chat_prompt | llm)


agent_with_memory = (
    RunnablePassthrough.assign(context=itemgetter('input')  | retriever | RunnableLambda(pp),
        chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter('history'),
        agent_scratchpad=RunnableLambda(itemgetter('intermediate_steps')) | format_to_openai_functions
    )
    # | RunnableLambda(pp)
    | chat_prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor_with_memory = AgentExecutor(agent=agent_with_memory, tools=tools, verbose=True)



input = """
What does Attention is all you need talk about?
"""
print(agent_executor_with_memory.invoke({'input':input}))