from fastapi import FastAPI;
from fastapi.responses import HTMLResponse
from . import router
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from NewsServer.scrap import main
from NewsServer.notifier import consume,produce
import schedule
from NewsServer import utils,models,schemas
from NewsServer.database import SessionLocal,engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler
models.Base.metadata.create_all(bind=engine)
scheduler=AsyncIOScheduler()
@asynccontextmanager
async def startup_event(app:FastAPI):
    scheduler.add_job(main,"cron",hour=13,minute=8)
    scheduler.start();
    yield
    scheduler.shutdown()
app=FastAPI(lifespan=startup_event);
app=FastAPI();
origins = [
  '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
async def Home():
    res='''
    <html>
        <body>
        <h2>News Service</h2>
        </body>
    </html>
    '''
    return HTMLResponse(res)


app.include_router(router.company_route)


# asyncio.create_task(main())

# asyncio.create_task(consume())

# asyncio.create_task(produce())