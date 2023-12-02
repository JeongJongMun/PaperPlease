import os
from embedchain import Pipeline as App

bot = App()

bot.add("https://arxiv.org/pdf/1810.04805.pdf")

bot.query("What is BERT?")