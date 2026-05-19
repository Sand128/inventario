from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas.auth import Token
from ..models.auth_models import User
from ..database import get_db
from pydantic import EmailStr
from ..utils.security import (
    verify_password,
    create_access_token,
    get_password_hash
)

router = APIRouter(tags=["auth"])

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400, 
            detail="Incorrect username or password"
        )
    token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register") 
def register_user(
    username: str, 
    email:EmailStr, 
    password: str, db: 
    Session = Depends(get_db)): 
    
    hashed_password = get_password_hash(password) 
    db_user = User( 
        username=username, 
        email=email, 
        hashed_password=hashed_password 
        ) 
    db.add(db_user) 
    db.commit() 
    db.refresh(db_user) 
    return {"message": "User registered successfully"}