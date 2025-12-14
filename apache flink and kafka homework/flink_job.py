from pyflink.table import TableEnvironment, EnvironmentSettings

X_MS = 60000
Y_MS = 30000
LATE_TOLERANCE_SECONDS = 5

WINDOW_SIZE_SEC = X_MS // 1000
WINDOW_SLIDE_SEC = Y_MS // 1000

BOOTSTRAP = "kafka:9093"
SENSORS_TOPIC = "sensors"
RESULTS1_TOPIC = "results1"
RESULTS2_TOPIC = "results2"


env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

t_env.get_config().set("table.exec.source.idle-timeout", "30 s")
t_env.get_config().set("parallelism.default", "1")

t_env.execute_sql(f"""
CREATE TABLE sensors (
  `key` STRING,
  `value` BIGINT,
  `timestamp` BIGINT,
  `event_time` AS TO_TIMESTAMP_LTZ(`timestamp`, 3),
  WATERMARK FOR event_time AS event_time - INTERVAL '{LATE_TOLERANCE_SECONDS}' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = '{SENSORS_TOPIC}',
  'properties.bootstrap.servers' = '{BOOTSTRAP}',
  'properties.group.id' = 'flink-sensors-group',
  'format' = 'json',
  'json.ignore-parse-errors' = 'true',
  'scan.startup.mode' = 'earliest-offset'
)
""")

t_env.execute_sql(f"""
CREATE TABLE {RESULTS1_TOPIC} (
  `key` STRING,
  window_start BIGINT,
  window_end   BIGINT,
  cnt BIGINT
) WITH (
  'connector' = 'kafka',
  'topic' = '{RESULTS1_TOPIC}',
  'properties.bootstrap.servers' = '{BOOTSTRAP}',
  'format' = 'json'
)
""")

t_env.execute_sql(f"""
CREATE TABLE {RESULTS2_TOPIC} (
  `key` STRING,
  window_start BIGINT,
  window_end   BIGINT,
  min_value BIGINT,
  `count` BIGINT,
  average DOUBLE,
  max_value BIGINT
) WITH (
  'connector' = 'kafka',
  'topic' = '{RESULTS2_TOPIC}',
  'properties.bootstrap.servers' = '{BOOTSTRAP}',
  'format' = 'json'
)
""")

table_result1 = t_env.execute_sql(f"""
INSERT INTO {RESULTS1_TOPIC}
SELECT
  `key`,
  CAST(
    UNIX_TIMESTAMP(DATE_FORMAT(window_start, 'yyyy-MM-dd HH:mm:ss')) * 1000
    AS BIGINT
  ) AS window_start,
  CAST(
    UNIX_TIMESTAMP(DATE_FORMAT(window_end, 'yyyy-MM-dd HH:mm:ss')) * 1000
    AS BIGINT
  ) AS window_end,
  COUNT(*) AS cnt
FROM TABLE(
  HOP(
    TABLE sensors,
    DESCRIPTOR(event_time),
    INTERVAL '{WINDOW_SLIDE_SEC}' SECOND,
    INTERVAL '{WINDOW_SIZE_SEC}' SECOND
  )
)
GROUP BY `key`, window_start, window_end
""")

table_result2 = t_env.execute_sql(f"""
INSERT INTO {RESULTS2_TOPIC}
SELECT
  `key`,
  CAST(
    UNIX_TIMESTAMP(DATE_FORMAT(window_start, 'yyyy-MM-dd HH:mm:ss')) * 1000
    AS BIGINT
  ) AS window_start,
  CAST(
    UNIX_TIMESTAMP(DATE_FORMAT(window_end, 'yyyy-MM-dd HH:mm:ss')) * 1000
    AS BIGINT
  ) AS window_end,
  MIN(`value`) AS min_value,
  COUNT(*)     AS `count`,
  AVG(CAST(`value` AS DOUBLE)) AS average,
  MAX(`value`) AS max_value
FROM TABLE(
  HOP(
    TABLE sensors,
    DESCRIPTOR(event_time),
    INTERVAL '{WINDOW_SLIDE_SEC}' SECOND,
    INTERVAL '{WINDOW_SIZE_SEC}' SECOND
  )
)
GROUP BY `key`, window_start, window_end
""")

print("Flink job started. Streaming from 'sensors' to 'results1' and 'results2'...")

import time

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("Stopping Flink job...")
