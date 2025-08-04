from fastapi import APIRouter, Path,Depends,HTTPException,Query,status
from fastapi.responses import JSONResponse
from users.schemas import *
from users.models import UserModel,TokenModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
import secrets

router = APIRouter(tags=["users"],prefix="/users") # show in docs

def generate_token(length=32):
    return secrets.token_hex(length)

@router.post("/login")
async def user_login(request:UserLoginSchema,db:Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=request.username.lower()).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="username not found")
    if not user_obj.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="wrong password")
    token_obj = TokenModel(user_id = user_obj.id, token=generate_token())
    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)
    return {"detail":"logged","token":token_obj.token}


@router.post("/register")
async def user_register(request:UserRegisterSchema,db:Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=request.username.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="username already exist")
    user_obj = UserModel(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    return JSONResponse(content={"details":"user created"})