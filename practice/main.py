from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
  
@app.get("/about")
async def about():
    return {"message": "This is a simple FastAPI application."}
  
@app.get("/hello/{name}")
async def helloFunction(name: str):
    return {"message": f"Hello {name}!"}
  
@app.get("/queryhello")
async def queryHelloFunction(name: str):
    return {"message": f"Hello {name}!"}
  
@app.get("/defaulthello")
async def defaultHelloFunction(name: Optional[str] = "World"):
    return {"message": f"Hello {name}!"}