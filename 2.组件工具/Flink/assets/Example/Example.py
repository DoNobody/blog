# 使用 StreamTableEnvironment
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.window import Slide, Tumble
from pyflink.table.expressions import lit, col
from pyflink.table.table_result import TableResult



def log_processing():
    env_settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
    t_env = StreamTableEnvironment.create(environment_settings=env_settings)
    # specify connector and format jars
    t_env.get_config().get_configuration().set_string("pipeline.jars", "file:///Users/liuhongwei/.m2/repository/org/apache/flink/flink-connector-kafka_2.11/1.12.0/flink-connector-kafka_2.11-1.12.0.jar;file:///Users/liuhongwei/.m2/repository/net/sf/json-lib/json-lib/2.3/json-lib-2.3-jdk15.jar;file:///Users/liuhongwei/.m2/repository/org/apache/kafka/kafka-clients/2.4.1/kafka-clients-2.4.1.jar")
    
    source_ddl = """
            CREATE TABLE source_table(
                token VARCHAR,
                stime BIGINT,
                appKey VARCHAR,
                user_action_time AS PROCTIME()
            ) WITH (
              'connector' = 'kafka',
              'topic' = 'markTopic',
              'properties.bootstrap.servers' = 'slavenode164.data.test.ds:9092,slavenode165.data.test.ds:9092,slavenode166.data.test.ds:9092',
              'properties.group.id' = 'test_3',
              'scan.startup.mode' = 'earliest-offset',
              'format' = 'json'
            )
            """

    sink_ddl = """
            CREATE TABLE sink_table(
                token VARCHAR,
                appKey VARCHAR,
                stime TIMESTAMP(3) NOT NULL,
                nums BIGINT NOT NULL
            ) WITH (
              'connector' = 'kafka',
              'topic' = 'markTopic1',
              'properties.bootstrap.servers' = 'slavenode164.data.test.ds:9092,slavenode165.data.test.ds:9092,slavenode166.data.test.ds:9092',
              'format' = 'json'
            )
            """

    t_env.execute_sql(source_ddl)
    t_env.execute_sql(sink_ddl)
    query_sql = """
        SELECT 
          token,
          appKey,
          TUMBLE_START(user_action_time, INTERVAL '5' MINUTE) as stime, 
          COUNT(token) as nums 
        FROM source_table 
        WHERE appKey = 'YSHAppAndroidIOSH5'
        GROUP BY 
          token,
          appKey,
          TUMBLE(user_action_time, INTERVAL '5' MINUTE)
    """
    # t_env.sql_query(query_sql) \
    #     .execute_insert("sink_table").wait()
    source_t = t_env.from_path("source_table")
    result = source_t.filter(source_t.appKey == "YSHAppAndroidIOSH5") \
      .window(Slide.over(lit(1).days) \
        .every(lit(1).minutes) \
        .on(source_t.user_action_time).alias("w")) \
        .group_by(source_t.token, source_t.appKey, col("w")) \
          .select(source_t.token, source_t.appKey, col("w").start.alias("stime"), source_t.token.count.alias("nums"))
    
    result.execute_insert("sink_table").wait()


if __name__ == '__main__':
    log_processing()