from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Blog(BaseModel):
    title : str
    body : str
    published: Optional[bool]

@app.get("/")
def home():
    return {"data": "blog list"}


# Path Parameters
@app.get("/blog/unpublished")
def unpublished():
    return {"data": "List of all unpublished blogs"}

@app.get("/blog/{id}")
def blog(id: int):
    return {"data": id}

@app.get("/blog/{id}/comment")
def comment(id):
    return {"data":{"1", "2"}}


# Query parameters
@app.get("/blog")
def index(limit: int = 10, published: bool = True, sort: Optional[str]=None):
    if published:
        return {"data": f'{limit} published blogs from the list'}
    
    return {"data": f'{limit} blogs from the list'}


# POST Method
@app.post("/create-blog")
def create_blog(blog: Blog):
    return {"data": f"blog is created with title {blog.title}"}
