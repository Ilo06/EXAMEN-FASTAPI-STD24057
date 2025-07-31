import base64
import datetime
from typing import List

from fastapi import FastAPI, Response, Request, HTTPException
from pydantic import BaseModel

app = FastAPI()


class PostModel(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime.datetime


posts_store: List[PostModel] = []


def serialized_posts():
    posts_converted = []
    for one_post in posts_store:
        posts_converted.append(one_post.model_dump())
    return posts_converted


@app.get("/ping")
def ping():
    return Response(content="pong", media_type="text/plain", status_code=200)


@app.get("/home")
def get_home():
    with open("home.html", "r") as f:
        html_content = f.read()
        return Response(content=html_content, status_code=200, media_type="text/html")


@app.post("/posts")
def post(event: list[PostModel]):
    posts_store.extend(event)
    return Response(status_code=201, content=str(serialized_posts()), media_type="application/json")


@app.get("/posts")
def get_all_posts():
    return serialized_posts()


@app.put("/posts")
def update_or_add_posts(new_posts: list[PostModel]):
    for new_post in new_posts:
        for i, existing_post in enumerate(posts_store):
            if existing_post.title == new_post.title:
                posts_store[i] = new_post
                break
        else:
            posts_store.append(new_post)
    return serialized_posts()


@app.get("/ping/auth")
def ping_auth(request: Request):
    auth = request.headers.get("Authorization")
    if not auth.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    encoded_credentials = auth.replace("Basic ", "")
    decoded = base64.b64decode(encoded_credentials).decode("utf-8")

    if decoded == "admin:123456":
        return Response(content="pong", media_type="text/plain", status_code=200)
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("notFound.html", "r", encoding="utf-8") as file:
        html_content = file.read()
        return Response(status_code=404, media_type="text/html", content=html_content)
