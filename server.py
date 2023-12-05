#!/usr/bin/env python

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from langserve import add_routes, RemoteRunnable
from langchain.schema.runnable import RunnableLambda
from langchain_utils import update_config, agent_executor, pp

app = FastAPI(
  title="Paper Please",
  version="1.0",
  description="AI Research Paper Chatbot Using LangChain",
)

# Mount the "static" directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Agent Input Must be a dict
# make_dict = lambda x: {'input': x}

def tt(x):
    print(type(x))
    return x

@app.get("/")
def read_root(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except HTTPException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
    
add_routes(
    app,
    RunnableLambda(tt) | RunnableLambda(pp) 
    | RunnableLambda(update_config)
    | agent_executor
    | RunnableLambda(pp),
    path="/chat",
    
)


"""Sample Questions
"Attention is All You Need"의 저자는 누구인가요?
2023년에 가장 인기 있는 AI 논문은 무엇인가요?
Attention is All You Need에 대해서 설명해줘.
BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding의 주된 주제에 대해서 설명해줘.
'GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding'의 저자는 누구인가요?
"""

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)