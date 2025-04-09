from fastapi import FastAPI

from .core.config import settings

app = FastAPI(
    debug=settings.DEBUG,
    root_path=settings.API_V1_STR,
)


@app.get("/hello-world")
def hello_world():
    return {"msg": "Hello, World!"}
