from fastapi import FastAPI;
from fastapi.responses import HTMLResponse
from . import router
import asyncio
from NewsServer.scrap import main
from NewsServer.notifier import consume,produce
import schedule
app=FastAPI();
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
asyncio.create_task(main())
asyncio.create_task(consume())
# asyncio.create_task(produce())