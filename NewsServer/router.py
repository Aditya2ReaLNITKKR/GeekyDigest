from fastapi import APIRouter
from NewsServer.scrap import main
import aioredis
import asyncio
import json
company_route=APIRouter()
redis=aioredis.Redis(host="localhost",port=6379,db=0)
@company_route.get('/news')
async def news():
    content=await redis.get('news-data')
    res=json.loads(content)
    print(res)
    return res
    # return 'hello world'
