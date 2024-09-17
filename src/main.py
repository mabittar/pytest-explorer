from __future__ import annotations

import os

import uvicorn

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel  # Corrigir importação

from core.calculator import Calculator


UVICORN_RELOAD = os.getenv("UVICORN_RELOAD", "False").lower() in ("true", "1")
UVICORN_HOST = os.getenv("UVICORN_HOST", "0.0.0.0")
UVICORN_PORT = int(os.getenv("UVICORN_PORT", "8000"))


class OperationBody(BaseModel):
    a: float | int
    b: float | int


class OperationResponse(BaseModel):
    result: float | int


app = FastAPI()


@app.get("/")
def index():
    return "Index Page"


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return "Checked"


@app.post("/api/add/", response_model=OperationResponse)
def add(body: OperationBody) -> OperationResponse:
    a = body.a
    b = body.b
    result = Calculator(a, b).add()
    return OperationResponse(result=result)


@app.post("/api/subtract/", response_model=OperationResponse)
def subtract(body: OperationBody) -> OperationResponse:
    a = body.a
    b = body.b
    result = Calculator(a, b).subtract()
    return OperationResponse(result=result)


@app.post("/api/multiply/", response_model=OperationResponse)
def multiply(body: OperationBody) -> OperationResponse:
    a = body.a
    b = body.b
    result = Calculator(a, b).multiply()
    return OperationResponse(result=result)


@app.post("/api/divide/", response_model=OperationResponse)
def divide(body: OperationBody) -> OperationResponse:
    a = body.a
    b = body.b
    if b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    result = Calculator(a, b).divide()
    return OperationResponse(result=result)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host=UVICORN_HOST, port=UVICORN_PORT, reload=UVICORN_RELOAD
    )
