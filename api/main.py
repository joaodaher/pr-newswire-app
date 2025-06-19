from fastapi import FastAPI

app = FastAPI(
    title="Wire Scout API",
    description="API for PR Newswire content",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Wire Scout API!"}
