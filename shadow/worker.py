#!/usr/bin/env python
import random
import uuid

import faust

from shadow import ShaDow


class HumanRating(faust.Record, serializer='json', include_metadata=False):
    rating: int
    unique_id: str


app = faust.App(
    'dominate-the-world',
    broker='kafka://localhost:9092',
    topic_partitions=3,
)

dominate_topic = app.topic('dominate', value_type=HumanRating)


@app.agent(dominate_topic)
async def detect_human_type(human_ratings):
    async for human_rating in human_ratings:
        print(human_rating)
        # ShaDow().worker(human_rating)


@app.timer(10)
async def producer_of_humans():
    for _ in range(10):
        await dominate_topic.send(value=HumanRating(
            rating=random.randint(0, 100),
            unique_id=str(uuid.uuid4())
        ))


if __name__ == '__main__':
    app.main()
