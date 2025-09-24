from fastapi import FastAPI
from app import models, schemas
from app.services import nlp, ocr, storage

app = FastAPI(title="MultiTools API Agent")

@app.get("/")
def root():
    return {"message": "MultiTools API Agent is running"}

@app.post("/analyze-text/")
def analyze_text(data: schemas.TextInput):
    return {"processed_text": nlp.process_text(data.text)}

@app.post("/extract-text/")
def extract_text(file: schemas.FileInput):
    return {"extracted_text": ocr.extract_text(file.file_path)}

@app.post("/store/")
def store_file(file: schemas.FileInput):
    return {"stored": storage.store_file(file.file_path)}
