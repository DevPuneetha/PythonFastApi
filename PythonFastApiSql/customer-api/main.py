from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Citizen

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Citizen API is running"
    }


@app.get("/citizens")
def get_citizens(db: Session = Depends(get_db)):
    citizens = db.query(Citizen).all()

    return citizens