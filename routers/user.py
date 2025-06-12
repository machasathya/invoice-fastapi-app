from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth,oauth2
from app.database import get_db


router = APIRouter()


@router.get("/users", response_model=List[schemas.UserShow])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.post("/users")
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pass = auth.hash(user.password)
    db_user = models.User(
        username=user.username,
        password=hashed_pass,
        user_type=user.user_type
    )
    db.add(db_user)
    db.commit()
    return {"message": "User created"}
