from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
import json
from NewsServer.config import KAFKA_TOPIC,KAFKA_BOOTSTRAP_SERVERS,loop,SERVER_EMAIL,SERVER_PASSWORD,RECEIVER_EMAIL
import asyncio
import smtplib,ssl
from email.message import EmailMessage
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
    print(str(msg[0][0]))
    body=f"Heading: {msg[0][0][0]} \n\n{msg[0][0][1]}"
    em=EmailMessage()
    em['From']=SERVER_EMAIL
    em['To']=RECEIVER_EMAIL
    em['subject']="Don't forget to subscribe"
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(SERVER_EMAIL,SERVER_PASSWORD)
        smtp.sendmail(SERVER_EMAIL,RECEIVER_EMAIL,em.as_string())



