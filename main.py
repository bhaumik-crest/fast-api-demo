from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()




@app.get("/")
def index():
    return {"message": "Hello World"}



