CREATE MATERIALIZED VIEW shadow_consumer
TO shadow
AS SELECT * FROM shadow_stream;
