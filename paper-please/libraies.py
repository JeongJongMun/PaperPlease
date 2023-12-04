import langchain
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import HumanMessagePromptTemplate

from PIL import Image
import matplotlib.pyplot as plt

import base64
import os
import fitz 
import io 