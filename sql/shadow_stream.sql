CREATE TABLE IF NOT EXISTS shadow_stream
(
    type String,
    unique_id String,
    emit_timestamp DateTime
) ENGINE = Kafka()
  SETTINGS
    kafka_broker_list = 'kafka:29092',
    kafka_topic_list = 'shadow',
    kafka_group_name = 'shadow-group',
    kafka_format = 'JSONEachRow',
    kafka_skip_broken_messages = 1;
