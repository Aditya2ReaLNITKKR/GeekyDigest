from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
import json
from NewsServer.config import KAFKA_TOPIC,KAFKA_BOOTSTRAP_SERVERS,loop,SERVER_EMAIL,SERVER_PASSWORD,RECEIVER_EMAIL
import asyncio
import smtplib,ssl
from email.message import EmailMessage
# from NewsServer import utils
from NewsServer.database import SessionLocal,engine
from sqlalchemy.orm import Session
# from NewsServer.router import get_db
from NewsServer import utils,models,schemas
from fastapi import Depends
models.Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
async def consume():
    consumer=AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        loop=loop
    )
    await consumer.start()
    try:
        async for msg in consumer:
            await email(json.loads(msg.value))
    finally:
        await consumer.stop()

async def produce(msg):
    producer=AIOKafkaProducer(loop=loop,bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        await producer.send(KAFKA_TOPIC,json.dumps(msg).encode('utf-8'))
    finally:
        await producer.stop()

async def email(msg):
    # print(str(msg[0][0]))
    body=f"Heading: {msg[0][1]} \n\n{msg[1][0]}\n\n{msg[2][0]} "
    em=EmailMessage()
    res=utils.get_users_email(db=next(get_db()),skip=0,limit=100)
    users_email=[user.email for user in res]
    print(users_email)
    em['From']=SERVER_EMAIL
    em['To']=','.join(users_email)
    em['subject']="Don't forget to subscribe"
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        await smtp.login(SERVER_EMAIL,SERVER_PASSWORD)
        await smtp.sendmail(SERVER_EMAIL,users_email,em.as_string())



