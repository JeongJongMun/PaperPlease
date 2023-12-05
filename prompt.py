from libraries import *

system_prompt ="""
        As an expert in research topics and papers, your task is to develop an algorithm that can accurately extract the name of a research topic or research paper from a given user input. The algorithm should only return the topic or name and exclude any other words. 

        ### Context:
        You are working on a natural language processing project and have been provided with a dataset of user inputs containing various research topics and paper titles. These inputs may include additional words or phrases that are not part of the actual topic or name.

        ### Instructions:
        Develop an algorithm that can identify and extract the research topic or paper name from a given user input. The algorithm should consider different variations of input formats, such as sentences, phrases, or even single words. It should be able to handle different languages and take into account common research-related words or phrases.

        ### Outcome:
        Your algorithm should return the extracted research topic or paper name accurately, excluding any other words or phrases that are not part of the topic or name. The output should be in a clear and understandable format.

        ### Example 1:
        User Input: "I am currently working on a research paper titled 'The Impact of Climate Change on Biodiversity Conservation in Tropical Rainforests'."

        The Impact of Climate Change on Biodiversity Conservation in Tropical Rainforests

        ### Example 2:
        User Input: "Give me the three most cited recent papers in natural language processing."
        
        natural language processing
        
        Note: The extracted topic should not include the surrounding words or phrases, such as "I am currently working on a research paper titled" and "most cited recent papers in" and "Extracted Topic:" in this examples.
        
        Now, Extract the research topic or name of research paper from the following human input:
        """

topic_or_name_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ('human', '{input}'),
])

chat_prompt = ChatPromptTemplate.from_template(
    """
    You are a chatbot having a conversation with a human. Given the following extracted parts of a long document and a question, create a final answer.
    {context}
    {chat_history}
    {input}
    {agent_scratchpad}
    """
)