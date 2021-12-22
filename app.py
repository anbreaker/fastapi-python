from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

app = FastAPI()

posts = []

# Post Model
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    create_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False


@app.get("/")
def read_root():
    return {"welcome": "Welcome to RestAPI py"}


@app.get("/posts")
def get_post():
    return posts


@app.post("/posts")
def save_post(post: Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]


@app.get("/post/{post_id}")
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    return HTTPException(status_code=404, detail="Post Not Found")


@app.put("/post/{post_id}")
def update_post(post_id: str, updatePost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = updatePost.title
            posts[index]["author"] = updatePost.author
            posts[index]["content"] = updatePost.content
            return {"message": "Post has been Updated successfully"}
    return HTTPException(status_code=404, detail="Post Not Found")


@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post has been deleted successfully"}
    return HTTPException(status_code=404, detail="Post Not Found")
