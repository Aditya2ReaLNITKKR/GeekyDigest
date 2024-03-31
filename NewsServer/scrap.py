from bs4 import BeautifulSoup;
import requests
import asyncio
import aiohttp
import json
from NewsServer.notifier import produce
import aioredis
redis=aioredis.Redis(host="localhost",port=6379,db=0)

urls=['https://www.jpmorgan.com/technology/technology-blog']

async def parse(content):
        soup= BeautifulSoup(content,'lxml')
        blocks=soup.find_all('div',class_='text cmp-text--light cmp-text--pt aem-GridColumn aem-GridColumn--default--12')
        res=[]
        for block in blocks:
            content=block.find('p').text
            heading=block.find('span').text
            # print(heading)
            res.append([heading,content])
        return res
async def fetch(session,url):
    async with session.get(url) as request:
        if request.status!=200:
             raise Exception(f"Failed to fetch {url}: {request.status}")
        
        content=await request.text()
        # print(content)
        res=await parse(content)
        return res


async def fetch_all(session,urls):
    tasks=[]
    for url in urls:
        task=asyncio.create_task(fetch(session,url))
        tasks.append(task)
    res=await asyncio.gather(*tasks)
    return res

async def check_update():
    content=await redis.get('news-data')
    res=json.loads(content)
    # print(res)
    await produce(res)
          

async def main():
    async with aiohttp.ClientSession() as session:
        res=await fetch_all(session,urls)
        await redis.set('news-data',json.dumps(res))
        await check_update()
        
# asyncio.run(main())

# html_content=requests.get('https://www.jpmorgan.com/technology/technology-blog').text
# soup=BeautifulSoup(html_content,'lxml')
# blocks=soup.find_all('div',class_='text cmp-text--light cmp-text--pt aem-GridColumn aem-GridColumn--default--12')

# for block in blocks:
#     content=block.find('p').text
#     print(heading)
#     print(content)
#     print('======')

