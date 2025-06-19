from fastapi import File, UploadFile, APIRouter

from database import SessionLocal, engine
from datetime import datetime
import pandas as pd

from .parser import parse_excel_file
from .categorizer import categorize_transactions
from models.models import Transaction


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

router = APIRouter(
    prefix ='/upload',
    tags=['Upload']
)

@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    contents = await file.read()
    path = f"./uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)

    # df = parse_excel_file(path)
    # df = categorize_transactions(df)

    # save_transactions_to_db(df)

    # return df.to_dict(orient="records")
    return "success"
