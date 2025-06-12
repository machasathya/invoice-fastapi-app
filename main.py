from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, auth, oauth2
from app.database import get_db, engine
from .routers import user, invoice




app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# --------------- User endpoints------------------

app.include_router(user.router, prefix="/api", tags=["Users"])

# --------------- Invoice enpoints ------------------
app.include_router(invoice.router, prefix="/api", tags=["invoice"])


# ---------------- Root ------------------

@app.get("/")
def root():
    return {"message": "Welcome to the Invoice App"}


# login

@app.post("/login")
def user_login(usercred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == usercred.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not auth.verify(usercred.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"token": access_token, "token_type": "bearer"}



