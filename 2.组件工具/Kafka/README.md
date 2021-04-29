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
