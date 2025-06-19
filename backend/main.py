from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from parser import parse_excel_file
from categorizer import categorize_transactions
import os
from database import SessionLocal, engine
from models import Transaction, Base
from datetime import datetime
import pandas as pd


app = FastAPI()

# Autoriser le frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crée les tables
Base.metadata.create_all(bind=engine)

def save_transactions_to_db(df: pd.DataFrame):
    db = SessionLocal()
    try:
        for _, row in df.iterrows():
            t = Transaction(
                date=row["date"].date() if isinstance(row["date"], datetime) else row["date"],
                description=row["description"],
                amount=row["amount"],
                category=row["category"]
            )
            db.add(t)
        db.commit()
    finally:
        db.close()

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    contents = await file.read()
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)

    df = parse_excel_file(path)
    df = categorize_transactions(df)

    save_transactions_to_db(df)

    return df.to_dict(orient="records")