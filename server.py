#!/usr/bin/env python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from langserve import add_routes
from langchain.schema.runnable import RunnableLambda
from agent import pp, tt,  agent_executor

app = FastAPI(
  title="Paper Please",
  version="1.0",
  description="AI Research Paper Chatbot Using LangChain",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

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
    RunnableLambda(pp)
    | agent_executor
    | RunnableLambda(pp),
    path="/chat",
    
)

"""Sample Questions
안녕! 정종문이야
너에 대해서 설명해줘
내 이름이 뭐라고?
2023년에 가장 인용이 많이 된 트렌드한 AI 연구 논문을 3가지정도 알려줘!
arXiv에서 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding'라는 논문의 링크를 주고, 논문의 내용을 간단하게 요약해줘.
Who is author of 'GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding'

arXiv에서 'ReAct: Synergizing Reasoning and Acting in Language Models'라는 논문을 찾아주고, 논문의 abstract를 요약해줘. ReAct는 Reasoning과 Acting을 언어 모델에 적용한거야. 

"""

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)