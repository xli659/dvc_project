from typing import Union 

from fastapi import FastAPI
# BaseModel from Pydantic is used to define data objects.
from pydantic import BaseModel

# Declare the data object with its components and their type.
class TaggedItem(BaseModel):
    name: str
    tags: Union[str, list] 
    item_id: int

app = FastAPI()
# Define a GET on the specified endpoint.
@app.get("/test")
async def say_hello():
    return {"greeting": "I dont have /"}

@app.get("/test/")
async def say_hello():
    return {"greeting": "I have /"}

@app.post("/items/")
async def create_item(item: TaggedItem):
    return item

@app.get("/items/{item_id}")
async def get_items(item_id: int, count: int = 1):
    return {"fetch": f"Fetched {count} of {item_id}"}

@app.post("/return/{test_path}")
async def exercise_function(test_path: str, query: str, body: TaggedItem):
  return {"path": test_path, "query": query, "body": body}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}

@app.get("/readinesscheck")
def readinesscheck():
    return {"status": "ready"}