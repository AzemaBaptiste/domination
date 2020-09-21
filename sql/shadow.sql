CREATE TABLE shadow as shadow_stream
ENGINE = MergeTree()
PARTITION BY toYYYYMM(emit_timestamp)
ORDER BY type;
