from fastapi import APIRouter
from NewsServer.scrap import main
import aioredis
from typing import List
import asyncio
import json
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from NewsServer import utils,models,schemas
from NewsServer.database import SessionLocal,engine
models.Base.metadata.create_all(bind=engine)
company_route=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
redis=aioredis.Redis(host="localhost",port=6379,db=0)
@company_route.get('/news')
async def news():
    content=await redis.get('news-data')
    res=json.loads(content)
    
    return res

@company_route.post('/users/',response_model=schemas.User)
def create_user(user:schemas.UserBase,db:Session=Depends(get_db)):
    db_user=utils.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400,detail="email already exist")
    return utils.create_user(db,user=user)

@company_route.get('/users/',response_model=List[schemas.User])
def read_user(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    users=utils.get_users(db,skip=skip,limit=limit)
    return users




