from fastapi import FastAPI

app = FastAPI(
    title="Basic FastAPI Assignment",
    description="Assignment 4 - Basic FastAPI App",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to my FastAPI application!"
    }


@app.get("/greet/{name}")
def greet(name: str):
    return {
        "message": f"Hello, {name}! Welcome to FastAPI."
    }


@app.get("/square/{number}")
def square(number: int):
    return {
        "number": number,
        "square": number * number
    }