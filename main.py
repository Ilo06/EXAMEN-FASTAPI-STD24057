from fastapi import FastAPI, Response

app = FastAPI()


# @app.get("/")
# def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# def say_hello(name: str):
#     return {"message": f"Hello {name}"}


@app.get("/ping")
def ping():
    return Response(content="pong", media_type="text/plain", status_code=200)

@app.get("/home")
def get_home():
    with open("home.html", "r") as f:
        html_content = f.read()
        return Response(content=html_content, status_code=200, media_type="text/html")



