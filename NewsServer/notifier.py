from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
import json
from NewsServer.config import KAFKA_TOPIC,KAFKA_BOOTSTRAP_SERVERS,loop
import asyncio
async def consume():
    consumer=AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        loop=loop
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed :")
    finally:
        await consumer.stop()

async def produce(msg):
    producer=AIOKafkaProducer(loop=loop,bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        await producer.send(KAFKA_TOPIC,json.dumps(msg).encode('utf-8'))
    finally:
        await producer.stop()