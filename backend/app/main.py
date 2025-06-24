from fastapi import FastAPI, UploadFile, File
from uuid import uuid4
import shutil
from . import storage, tasks

app = FastAPI(title="Knowledge Vault")


@app.get("/")
async def root():
    return {"message": "Knowledge Vault API"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    doc_id = str(uuid4())
    dest = storage.UPLOAD_DIR / f"{doc_id}_{file.filename}"
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    docs = storage.load_documents()
    docs.append({"id": doc_id, "filename": file.filename})
    storage.save_documents(docs)

    tasks.process_document.delay(doc_id)

    return {"id": doc_id, "filename": file.filename}


@app.get("/documents")
async def list_documents():
    return storage.load_documents()
