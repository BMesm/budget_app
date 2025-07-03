from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import upload_file
from database import Base, engine

app = FastAPI()

# Autoriser le frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_file.router)

# Crée les tables
Base.metadata.create_all(bind=engine)

@app.get("/ping")
def ping():
    return {"message": "pong"}