#!/usr/bin/env python

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from langserve import add_routes, RemoteRunnable

from langchain_utils import agent_executor, pp
from libraries import *

app = FastAPI(
  title="Paper Please",
  version="1.0",
  description="AI Research Paper Chatbot Using LangChain",
)

# Mount the "static" directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Agent Input Must be a dict
make_dict = lambda x: {'input': x}

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
    RunnableLambda(make_dict) | RunnableLambda(pp) | agent_executor | RunnableLambda(pp),
    path="/chat",
    
)

"""Sample Questions
Who is the Author of "Attention is All You Need"?
Which AI Paper is Hottest in 2023? Describe it in 3 sentences.
Tell me about Attention is All You Need. Describe it in 3 sentences.
Who is the Author of 'GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding'?
"""

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001)