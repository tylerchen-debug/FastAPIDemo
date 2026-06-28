from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def root():
    return "Welcome to FastAPI Demo"


@app.get("/hello")
def hello():
    return "Hello from FastAPI"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
