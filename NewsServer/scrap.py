from bs4 import BeautifulSoup;
import requests
import asyncio
import aiohttp
import json
from NewsServer.notifier import produce
import aioredis
redis=aioredis.Redis(host="localhost",port=6379,db=0)

# urls=['https://www.jpmorgan.com/technology/technology-blog','https://www.intuit.com/blog/category/innovative-thinking/tech-innovation/','https://techcommunity.microsoft.com/t5/custom/page/page-id/Blogs']
async def parse_intuit(session):
      url= 'https://www.intuit.com/blog/category/innovative-thinking/tech-innovation/'
      async with session.get(url) as request:
        if request.status!=200:
             raise Exception(f"Failed to fetch {url}: {request.status}")
        
        content=await request.text()
       
        res=[]
        soup=BeautifulSoup(content,'lxml')
        blocks=soup.find_all('a',class_='rkv-card__link')
        for block in blocks:
            content=block.get('aria-label')
            link=block.get('href')
            dict={
                  "link":link,
                  "title":'Innovative Thinking',
                 "body":content,
            }
            res.append(dict)
        return res
async def parse_jpmorgan(session):
        url= 'https://www.jpmorgan.com/technology/technology-blog'
        async with session.get(url) as request:
            if request.status!=200:
                raise Exception(f"Failed to fetch {url}: {request.status}")
            
            content=await request.text()
        res=[]
        soup= BeautifulSoup(content,'lxml')
        blocks=soup.find_all('div',class_='cmp-text')
        for block in blocks:
             title_name=''
             title=block.find('span',class_='title-large')
             if title:
                  title_name=title.text
             body_tag=block.find('p')
             body=''
             if body_tag:
                  body=block.find('p').text
             a_tag=block.find('a',class_='chaseanalytics-track-link')
             link='https://www.jpmorgan.com'
             if a_tag:
                  link= block.find('a',class_='chaseanalytics-track-link').get('href')
                  link='https://www.jpmorgan.com'+link
             dict={
                  "link":link,
                  "title":title_name,
                  "body":body,
             }
             res.append(dict)
        return res
async def parse_microsoft(session):
        url= 'https://techcommunity.microsoft.com/t5/custom/page/page-id/Blogs'
        async with session.get(url) as request:
            if request.status!=200:
                raise Exception(f"Failed to fetch {url}: {request.status}")
            
            content=await request.text()
        res=[]
        soup= BeautifulSoup(content,'lxml')
        blocks=soup.find_all('div',class_='item')
        for block in blocks:
             link=block.find('div',class_='blog-title').find('a').get('href')
             title=block.find('span',class_='blog-name').find('a').get_text(strip=True)
             body=block.find('div',class_='details').find('div',class_='body').get_text(strip=True)
             dict={
                  "link":'https://techcommunity.microsoft.com'+link,
                  "title":title,
                  "body":body
             }
             res.append(dict)
      
        return res
async def fetch_all(session):
    tasks=[]
    # asyncio.create_task(fetch(session,url))
    tasks.append(asyncio.create_task(parse_jpmorgan(session)))
    tasks.append(asyncio.create_task(parse_intuit(session)))
    tasks.append(asyncio.create_task(parse_microsoft(session)))
    res=await asyncio.gather(*tasks)
    return res

async def check_update(res):
    content=await redis.get('news-data')
    if content is None:
         await redis.set('news-data',json.dumps(res))
    
    else:
         prev_res=json.loads(content)
     #     print(prev_res[0][1]['title'])
     #     print(res[0][1]['title'])
         if prev_res[0][1]['title'] != res[0][1]['title'] or prev_res[1][0]['title'] != res[1][0]['title'] or prev_res[2][0]['title'] != res[2][0]['title']:
              print(' change')
              await redis.set('news-data',json.dumps(res))
              await produce(res)


async def main():
    async with aiohttp.ClientSession() as session:
        res=await fetch_all(session)
        await check_update(res)
     #    print(res)
     # #    return res
     #    await redis.set('news-data',json.dumps(res))
        
# asyncio.run(main())

# html_content=requests.get('https://www.jpmorgan.com/technology/technology-blog').text
# soup=BeautifulSoup(html_content,'lxml')
# blocks=soup.find_all('div',class_='text cmp-text--light cmp-text--pt aem-GridColumn aem-GridColumn--default--12')

# for block in blocks:
#     content=block.find('p').text
#     print(heading)
#     print(content)
#     print('======')

