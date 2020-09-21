Domination
==========

Real-time application made to monitor and dominate Humans.

From the rating of every human (from 1 to 100) sent to the kafka topic `dominate`,
 we detect, in real time, which type they are:
 - `Sha` if its rating is a multiple of 3
 - `Dow` if its rating is a multiple of 5
 - `ShaDow` if its rating is a multiple of 3 and 5
 - `Incompatible` if none of the above.
 
Using a new kafka topic `shadow`, we make the result available to a clickhouse 
table named `shadow`.



## System Design
    
    +----------------+               +-------------+            +------------------+
    |  domination    |               |  dominate   |            | domination       |
    +----------------+               +-------------+            +------------------+
    | python         | +-----------> |             | +--------> | python           |
    | Faust producer |               | Kafka topic |            | Faust agent      |
    | HumanRatings   |               |             |            | HumanCategorized |
    +----------------+               +-------------+            +------------------+
                                                                          +
                                                                          |
          +---------------------------------------------------------------+
          |
          v
    +----------------+           +-------------------+           +-------------------+
    |  shadow        |           | shadow_stream     |           |  shadow_consumer  |
    +----------------+           +-------------------+           +-------------------+
    |                | +------>  | clickhouse table  | +------>  | clickhouse table  |
    |  Kafka topic   |           | encapsulate topic |           | materialized view |
    |                |           |                   |           |                   |
    +----------------+           +-------------------+           +-------------------+
                                                                          +
                                                                          |
          +---------------------------------------------------------------+
          |
          v
    +-------------------+
    |  shadow           |
    +-------------------+
    | clickhouse table  |
    | store rows        |
    |                   |
    +-------------------+


Structure of Kafka messages:
- topic `dominate`:
    `{"rating": <integer>, "unique_id": "<string>"}`


- topic `shadow`:
    `{"type": <integer>, "unique_id": "<string>", "emit_timestamp": <datetime>}`


## Requirements

- Python >= 3.6
- docker-compose

## Usage

    pip install domination
    
    # Start domination
    docker-compose up -d
    domination worker -l info
    
    # Stop domination
    Ctrl + C
    docker-compose down
    
    # In case of Kafka broker errors occur:
    docker-compose rm && docker-compose up -d  # recreate containers

You can also run The Algorithm as a standalone. It will print the type 
of every human rated from 1 to 1337.

    python the_algorithm.py 
    
## Development

    # Install
    virtualenv -p python3.8 venv
    source venv/bin/activate
    pip install -r requirements.txt
    make install
    
    # Build
    make test # coverage tests
    make linter # runs pylint
    make build

#### Create clickhouse tables

Open CLI of the clickhouse client

    docker exec -it clickhouse bin/bash -c "clickhouse-client --multiline"

Create shadow_stream, shadow and shadow_consumer tales

    CREATE TABLE IF NOT EXISTS shadow_stream
    (
        `type` String,
        `unique_id` String,
        `emit_timestamp` DateTime
    ) ENGINE = Kafka()
      SETTINGS
        kafka_broker_list = 'kafka:29092',
        kafka_topic_list = 'shadow',
        kafka_group_name = 'shadow-group',
        kafka_format = 'JSONEachRow',
        kafka_skip_broken_messages = 1;
    

    CREATE TABLE shadow as shadow_stream
    ENGINE = MergeTree()
    PARTITION BY toYYYYMM(emit_timestamp)
    ORDER BY type;


    CREATE MATERIALIZED VIEW shadow_consumer 
    TO shadow
    AS SELECT * FROM shadow;
    
You can now explore your data

    SELECT COUNT(*) AS COUNT, type FROM shadow
     GROUP BY type ORDER BY (COUNT) DESC LIMIT 10;

## References
- [blog.streamthoughts.fr](https://blog.streamthoughts.fr/2020/06/creer-une-plateforme-analytique-temps-reel-avec-kafka-ksqldb-et-clickhouse/)
- [medium.com](https://medium.com/big-data-engineering/hello-kafka-world-the-complete-guide-to-kafka-with-docker-and-python-f788e2588cfc)

## TODO
 - deploy package to pypi using github actions
