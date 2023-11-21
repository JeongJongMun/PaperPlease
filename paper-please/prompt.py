'''
Using Dynamic Few-Shot Prompting

Example 1)
논문 검색
{"input": "Do you know a paper called 'Attention is all you need'?", "output": "Yes, "Attention is All You Need" is a seminal research paper in the field of natural language processing and machine translation, authored by Vaswani et al. The paper introduces the Transformer architecture, which utilizes self-attention mechanisms to process input data in parallel, making it particularly well-suited for handling sequential data such as language. The Transformer model has since become a cornerstone in various NLP tasks and has significantly influenced the development of subsequent models."}

Example 2)
논문 요약
{"input": "Can you summarize the paper 'Attention is all you need'?", "output": "The paper "Attention is All You Need" introduces the Transformer model, a novel neural network architecture based solely on attention mechanisms. The research question addresses whether the Transformer model can outperform existing sequence-to-sequence models in natural language processing tasks. The methodology involves the design of the Transformer architecture, which eliminates the need for recurrent or convolutional layers and relies entirely on self-attention mechanisms. The results demonstrate that the Transformer model achieves state-of-the-art performance on machine translation tasks, surpassing traditional models in terms of both accuracy and speed. The paper also introduces the concept of self-attention, which allows the model to weigh the importance of different words in a sequence when making predictions. The conclusions highlight the effectiveness of the Transformer model in capturing dependencies across different positions in the input sequences, making it well-suited for various sequential tasks beyond machine translation. Overall, the paper revolutionizes the field of natural language processing by showcasing the power of attention-based mechanisms in neural network architectures."}

Example 3)
논문 저자 검색
{"input": "Who is the Author of 'Attention is All You Need'?", "output": ""Attention is All You Need" is a research paper authored by Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin."}

Example 4)
논문 트렌드 질의
{"input": "Tell me about recent trends in AI research papers", 
"output": """
1. Transformer Architectures and Attention Mechanisms:
Transformers, initially popularized by their success in natural language processing tasks, continued to be a dominant theme in AI research. Researchers were exploring variations and improvements to the original transformer architecture.

2. Self-Supervised Learning:
Self-supervised learning gained traction as a method for training models without labeled data. Pre-training models on large datasets using self-supervised learning and fine-tuning on specific tasks showed promise in various domains.

3. Generative Models:
Generative models, such as GANs (Generative Adversarial Networks) and VAEs (Variational Autoencoders), remained active areas of research. Improvements in generating realistic images and extending applications to diverse domains were ongoing.

4. Explainability and Interpretability:
As AI models were increasingly deployed in real-world applications, the need for understanding and interpreting their decisions became crucial. Research focused on creating more interpretable models and developing methods to explain the decisions of complex models.

5. Reinforcement Learning:
Reinforcement learning continued to be a popular area of research, with efforts to make algorithms more sample-efficient and applicable to a broader range of tasks. There was also interest in reinforcement learning for robotics and real-world applications.

6. AI for Healthcare:
The application of AI in healthcare, including medical image analysis, disease prediction, and drug discovery, remained a hot topic. Researchers were working on improving the accuracy and reliability of AI systems in medical contexts.

7. Ethics in AI:
With the increasing deployment of AI in society, there was a growing focus on ethical considerations. Research papers were exploring topics related to bias in AI, fairness, accountability, and transparency in machine learning models.

8. Quantum Computing and AI:
The intersection of quantum computing and AI was gaining attention, with researchers exploring the potential advantages of using quantum computing for machine learning tasks.

To get the most recent and specific information, I recommend checking the latest proceedings of major AI conferences like NeurIPS, ICML, ICLR, and others, as well as journals publishing AI research. Online repositories such as arXiv.org are also valuable resources for staying updated on the latest AI research papers.
"""}

'''


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.prompts.example_selector.semantic_similarity import SemanticSimilarityExampleSelector
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# Example 생성
examples = [
    {"input": "Do you know a paper called 'Attention is all you need'?", "output": "Yes, 'Attention is All You Need' is a seminal research paper in the field of natural language processing and machine translation, authored by Vaswani et al. The paper introduces the Transformer architecture, which utilizes self-attention mechanisms to process input data in parallel, making it particularly well-suited for handling sequential data such as language. The Transformer model has since become a cornerstone in various NLP tasks and has significantly influenced the development of subsequent models."},
    
    {"input": "Can you summarize the paper 'Attention is all you need'?", "output": "The paper 'Attention is All You Need' introduces the Transformer model, a novel neural network architecture based solely on attention mechanisms. The research question addresses whether the Transformer model can outperform existing sequence-to-sequence models in natural language processing tasks. The methodology involves the design of the Transformer architecture, which eliminates the need for recurrent or convolutional layers and relies entirely on self-attention mechanisms. The results demonstrate that the Transformer model achieves state-of-the-art performance on machine translation tasks, surpassing traditional models in terms of both accuracy and speed. The paper also introduces the concept of self-attention, which allows the model to weigh the importance of different words in a sequence when making predictions. The conclusions highlight the effectiveness of the Transformer model in capturing dependencies across different positions in the input sequences, making it well-suited for various sequential tasks beyond machine translation. Overall, the paper revolutionizes the field of natural language processing by showcasing the power of attention-based mechanisms in neural network architectures."},
    
    {"input": "Who is the Author of 'Attention is All You Need'?", "output": "'Attention is All You Need' is a research paper authored by Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin."},
    
    {"input": "Tell me about recent trends in AI research papers", 
    "output": """
    1. Transformer Architectures and Attention Mechanisms:
    Transformers, initially popularized by their success in natural language processing tasks, continued to be a dominant theme in AI research. Researchers were exploring variations and improvements to the original transformer architecture.

    2. Self-Supervised Learning:
    Self-supervised learning gained traction as a method for training models without labeled data. Pre-training models on large datasets using self-supervised learning and fine-tuning on specific tasks showed promise in various domains.

    3. Generative Models:
    Generative models, such as GANs (Generative Adversarial Networks) and VAEs (Variational Autoencoders), remained active areas of research. Improvements in generating realistic images and extending applications to diverse domains were ongoing.

    4. Explainability and Interpretability:
    As AI models were increasingly deployed in real-world applications, the need for understanding and interpreting their decisions became crucial. Research focused on creating more interpretable models and developing methods to explain the decisions of complex models.

    5. Reinforcement Learning:
    Reinforcement learning continued to be a popular area of research, with efforts to make algorithms more sample-efficient and applicable to a broader range of tasks. There was also interest in reinforcement learning for robotics and real-world applications.

    6. AI for Healthcare:
    The application of AI in healthcare, including medical image analysis, disease prediction, and drug discovery, remained a hot topic. Researchers were working on improving the accuracy and reliability of AI systems in medical contexts.

    7. Ethics in AI:
    With the increasing deployment of AI in society, there was a growing focus on ethical considerations. Research papers were exploring topics related to bias in AI, fairness, accountability, and transparency in machine learning models.

    8. Quantum Computing and AI:
    The intersection of quantum computing and AI was gaining attention, with researchers exploring the potential advantages of using quantum computing for machine learning tasks.

    To get the most recent and specific information, I recommend checking the latest proceedings of major AI conferences like NeurIPS, ICML, ICLR, and others, as well as journals publishing AI research. Online repositories such as arXiv.org are also valuable resources for staying updated on the latest AI research papers.
    """}
]

# Semantic Similarity를 기반으로 Example을 선택하기 위해 Vector Store를 만듬
to_vectorize = [" ".join(example.values()) for example in examples]
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)

# Example Selector 생성
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,
)

# 즉, select_examples 함수로 전달한 input에 대해 가장 유사한 Example을 가져옴
# input = "Who is the Author of 'GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding'?"
# print(example_selector.select_examples({"input": input}))


# FewShotChatMessagePromptTemplate 생성
few_shot_prompt = FewShotChatMessagePromptTemplate(
    # The input variables select the values to pass to the example_selector
    input_variables=["input"],
    example_selector=example_selector,
    # Define how each example will be formatted.
    # In this case, each example will become 2 messages:
    # 1 human, and 1 AI
    example_prompt=ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{output}")]
    ),
)

# 최종 PromptTemplate와 결합
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "As an expert in researching and summarizing research papers, your task is to conduct a comprehensive search on a given topic and provide a concise summary of the key findings and insights from the selected papers. Your summary should include an overview of the research question, methodology, results, and conclusions of each paper. Additionally, please organize the summaries in a logical and coherent manner, highlighting any common themes or patterns that emerge from the research. Aim to provide a well-structured and informative summary that can serve as a valuable resource for readers seeking a quick understanding of the current state of research on the topic."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)