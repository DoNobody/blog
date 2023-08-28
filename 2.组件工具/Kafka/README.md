[首页](/)
# Kafka

## 用的一些命令

```shell
# 查看topic下的每个partition的offset进度
./bin/kafka-run-class.sh kafka.tools.GetOffsetShell --topic logmonitor --time -1 --broker-list kafka01.prod.data.phd2.jianlc.jlc:9092 --partitions 0

# 如出现Leader 未 -1的情况：
# broker shutdown的时候，partition的leader在此broker上，controller选主没有成功，移除此broker后，对应的partition的leader就被赋值成-1了
# 重新启动broker即可。

# 查看当前的消费组
./bin/kafka-consumer-groups.sh --bootstrap-server 10.10.31.5:9091 --list
./bin/kafka-consumer-groups.sh --describe --bootstrap-server 10.11.31.5:9091 --group cloudera_mirrormaker

```

## 使用命令kafka-reassign-partitions.sh在broker上重新分布partition

- 新建一个`topic-generate.json` 文件，写入需要处理的topic

```json
{
  "topics": [
    {
      "topic": "radarlog"
    }
  ],
  "version": 1
}
```

- 使用命令生成推荐的 partition分区信息。

```shell
# 使用命令
./bin/kafka-reassign-partitions.sh --zookeeper 127.0.0.1:2181 --topics-to-move-json-file topic-generate.json --broker-list "0,1,3" --generate

# 返回
Current partition replica assignment
{"version":1,"partitions":[{"topic":"radarlog","partition":2,"replicas":[3,0]},{"topic":"radarlog","partition":7,"replicas":[1,3]},{"topic":"radarlog","partition":0,"replicas":[0,1]},{"topic":"radarlog","partition":4,"replicas":[1,0]},{"topic":"radarlog","partition":1,"replicas":[1,3]},{"topic":"radarlog","partition":6,"replicas":[0,1]},{"topic":"radarlog","partition":5,"replicas":[3,1]},{"topic":"radarlog","partition":3,"replicas":[0,3]}]}

Proposed partition reassignment configuration
{"version":1,"partitions":[{"topic":"radarlog","partition":2,"replicas":[1,0]},{"topic":"radarlog","partition":7,"replicas":[0,3]},{"topic":"radarlog","partition":4,"replicas":[0,1]},{"topic":"radarlog","partition":0,"replicas":[3,1]},{"topic":"radarlog","partition":6,"replicas":[3,1]},{"topic":"radarlog","partition":1,"replicas":[0,3]},{"topic":"radarlog","partition":5,"replicas":[1,3]},{"topic":"radarlog","partition":3,"replicas":[3,0]}]}
```

- 使用将推荐的partition reassignment configuration 写入 partition-replica-reassignment.json 文件

```json
# cat partition-replica-reassignment.json
{"version":1,"partitions":[{"topic":"radarlog","partition":2,"replicas":[1,0]},{"topic":"radarlog","partition":7,"replicas":[0,3]},{"topic":"radarlog","partition":4,"replicas":[0,1]},{"topic":"radarlog","partition":0,"replicas":[3,1]},{"topic":"radarlog","partition":6,"replicas":[3,1]},{"topic":"radarlog","partition":1,"replicas":[0,3]},{"topic":"radarlog","partition":5,"replicas":[1,3]},{"topic":"radarlog","partition":3,"replicas":[3,0]}]}
```

- 使用命令kafka-reassign-partitions.sh进行`执行`

```shell
./bin/kafka-reassign-partitions.sh --zookeeper 127.0.0.1:2181 --reassignment-json-file partition-replica-reassignment.json --execute
```

- 使用kafka-reassign-partitions.sh查询`状态`

```shell
./bin/kafka-reassign-partitions.sh --zookeeper 127.0.0.1:2181 --reassignment-json-file partition-replica-reassignment.json --verify
```
