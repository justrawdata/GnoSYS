from fastapi import FastAPI

app = FastAPI(title="Knowledge Vault")

@app.get("/")
async def root():
    return {"message": "Knowledge Vault API"}
