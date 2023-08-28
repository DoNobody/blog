# hive 的基础知识

## 问题

- > FAILED: SemanticException [Error 10265]: This command is not allowed on an ACID table test_db.test_table with a non-ACID transaction manager. Failed command: null

```bash
# Hive transaction manager must be set to org.apache.hadoop.hive.ql.lockmgr.DbTxnManager in order to work with ACID tables.
SET hive.txn.manager=org.apache.hadoop.hive.ql.lockmgr.DbTxnManager;

#Additionally, Set these properties to turn on transaction support
# Client Side
SET hive.support.concurrency=true;
SET hive.enforce.bucketing=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

# Server Side (Metastore)
SET hive.compactor.initiator.on=true;
SET hive.compactor.worker.threads=1;

# Note: Add these properties in hive-site.xml to set them permanently.
```

- > hive 中如何去正则匹配列

```bash
set hive.support.quoted.identifiers=None;
select `(name|id|pwd)?+.+` from tableName;
```

- > hive 中设置参数：

```bash
set hive.execution.engine=spark;
set spark.executor.memory=8g;
```

### hive 中行转列

> 原始数据

| id  | goods                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 80  | `[{"floorImgUrl":"https://hotwheel-static.jianlc.com/shop/20201230/1609299782739.png","floorExhibitionMode":2,"goods":[{"goodId":"64686117450","channel":1,"jxCashGiftId":"5160ea3579bc6f43","cashGiftAmount":5,"cashGiftStartTime":"2020.12.30 00:00","cashGiftEndTime":"2021.01.05 23:59"},{"goodId":"30808459309","channel":1,"jxCashGiftId":"c9672e705444178a","cashGiftAmount":5,"cashGiftStartTime":"2020.12.30 00:00","cashGiftEndTime":"2021.01.05 23:59"}]}]` |

> SQL 处理过程

```sql
select
id,
regexp_extract(json1,'"goodId":"([\\d_-]*)"', 1) as goodId,
regexp_extract(json1,'"channel":([\\d_-]*)', 1) as channel,
regexp_extract(json1,'"jxCashGiftId":"([a-zA-Z0-9]*)"', 1) as jxCashGiftId,
regexp_extract(json1,'"cashGiftAmount":([\\d_-]*)', 1) as cashGiftAmount,
regexp_extract(json1,'"cashGiftStartTime":"([\\d\.\\s:]*)"', 1) as cashGiftStartTime,
regexp_extract(json1,'"cashGiftEndTime":"([\\d\.\\s:]*)"', 1) as cashGiftEndTime
from
(select id,json1 from activity_content
lateral view  explode(split(regexp_replace(get_json_object(goods, '$[*].goods[*]'),'\\[\\{|\\\\}]',''),'\\}\\,\\{')) js as json1
where id = 80
) tmp
```

> 处理后

| id  | goodid      | channel | jxCashGiftId     | cashGiftAmount | cashGiftStartTime | cashGiftEndTime  |
| --- | ----------- | ------- | ---------------- | -------------- | ----------------- | ---------------- |
| 80  | 64686117450 | 1       | 5160ea3579bc6f43 | 5              | 2020.12.30 00:00  | 2021.01.05 23:59 |
| 80  | 30808459309 | 1       | c9672e705444178a | 5              | 2020.12.30 00:00  | 2021.01.05 23:59 |

## hive 中大数据量优化历程

### 千亿级别的查询优化

> [漫谈千亿级数据优化实践：一次数据优化实录](https://cloud.tencent.com/developer/article/1042700)

- 分区
- 索引
- 分桶
- 活跃度区分
- 新的数据结构

### 数据倾斜问题

- 表象
  - 用 Hive 算数据的时候 reduce 阶段卡在 99.99%
  - 用 SparkStreaming 做实时算法时候，一直会有 executor 出现 OOM 的错误，但是其余的 executor 内存使用率却很低。
  - 数据量大，单台机器完全无法处理。
  - hadoop 中的数据倾斜
    - 有一个或多个 reduce 卡住
    - 各种 container 报错 OOM
    - 读写的数据量极大，至少远远超过其它正常的 reduce
  - Spark 中的数据倾斜
    - Executor lost，OOM，Shuffle 过程出错
    - Driver OOM
    - 单个 Executor 执行时间特别久，整体任务卡在某个阶段不能结束
    - 正常运行的任务突然失败
    - Spark streaming 程序：map,join 方法中出现 OOM
- 原因
  - 计算过程中需要在单独一个节点上计算
  - 不合理的 shuffle 方式
  - 数据本身倾斜很严重
- 解决
  - 业务场景
    - 业务逻辑场景
      - 有损处理： 删除过滤
      - 无损处理： 对分布不均匀的数据单独计算，先打散再汇聚
      - 数据预处理
    - 程序优化、调整参数
      - 采用 map join
      - count distinct 的操作，先转成 group，再 count
      - hive.groupby.skewindata=true
      - left semi jioin 的使用
      - 设置 map 端输出、中间结果压缩
