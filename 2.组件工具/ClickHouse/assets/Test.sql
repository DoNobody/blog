-- 新建表ReplacingMergeTree
CREATE TABLE message_notify
(
    `uid` UInt64,
    `message_id` String,
    `when` DateTime,
    `message` String,
    `acked` UInt8 DEFAULT 0,
    `ack_time` DateTime DEFAULT toDateTime(0)
)
ENGINE = ReplacingMergeTree(ack_time)
PARTITION BY toYYYYMM(when)
ORDER BY (uid, when, message_id)

-- 插入模拟数据
INSERT INTO message_notify (
        uid,
        message_id,
        when,
        message
    )
SELECT toUInt64((rand(1) % 1000) + 1) AS uid,
    randomPrintableASCII(64) AS message_id,
    toDateTime('2021-03-15 00:00:00') + (rand(2) % ((3600 * 24) * 30)) AS
    when,
    randomPrintableASCII(1024) AS message
from numbers(10000000000)

INSERT INTO message_notify (
        uid,
        message_id,
        when,
        message,
        acked,
        ack_time
    )
SELECT uid,
    message_id,
    when,
    message,
    1 AS acked,
    now() as ack_time
from message_notify
where (cityHash64(message_id) % 99) != 0



-- 验证插入数据
select count()
from message_notify

select count()
from message_notify final

-- 查看用户未读数据

select count(),
    sum(cityHash64(*)) as data
from (
        select uid,
            message_id,
            when,
            argMax(message, ack_time) as message,
            argMax(acked, ack_time) as acked,
            max(ack_time) as ack_time_
        from message_notify
        group by uid,
            message_id,
            when
    )
where uid = 520
    and not acked

-- 新建表AggregatingMergeTree
CREATE TABLE message_notify_new (
    `uid` UInt64,
    `message_id` String,
    `when` DateTime,
    `message` SimpleAggregateFunction(max, String),
    `acked` SimpleAggregateFunction(max, String),
    `ack_time` SimpleAggregateFunction(max, String)
) ENGINE = AggregatingMergeTree() PARTITION BY toYYYYMM(
    when
)
ORDER BY (
        uid,
        when,
        message_id
    ) settings enable_vertical_merge_algorithm = 10,
    vertical_merge_algorithm_min_rows_to_activate = 10,
    vertical_merge_algorithm_min_columns_to_activate = 10


-- alter 修改表类型

alter table message_notify_new modify column acked SimpleAggregateFunction(max, UInt8)  after message; 
alter table message_notify_new modify column ack_time SimpleAggregateFunction(max, DateTime)  after acked; 

show create table message_notify_new

-- 准备数据
insert into message_notify_new select * from message_notify where not acked

insert into message_notify_new
select 
uid,
message_id,
when,
'' as message,
acked,
ack_time
from message_notify
where acked

select count() from message_notify_new final;
/* 用于回收闲置的数据库空间，当表上的数据行被删除时，
所占据的磁盘空间并没有立即被回收，使用了OPTIMIZE TABLE命令后这些空间将被回收，
并且对磁盘上的数据行进行重排 */
optimize table message_notify_new

-- 查看分区表的信息
SELECT partition,name,active,part_type FROM system.parts WHERE table = ''

-- 查询
select count(),
    sum(cityHash64(*)) as data
from (
        select uid,
            message_id,
            when,
            max(message) as message,
            max(acked) as acked,
            max(ack_time) as ack_time_
        from message_notify_new
        group by uid,
            message_id,
            when
    )
where (uid = 520)
    and (not acked)

-- 查看当前的settings
SELECT * FROM system.settings where name like 'log_queries%'

show create table user_amount_fact

show databases

use user_trade_fact
show tables


CREATE TABLE IF NOT EXISTS user_trade_fact.user_amount_fact
(
    `user_id` String,
    `biz` String,
    `series` String,
    `dim` String,
    `amount` Float64,
    `part_log_day` String
)ENGINE = MergeTree
PARTITION BY part_log_day
ORDER BY (biz,series,dim,user_id)
SETTINGS old_parts_lifetime = 60

-- 使用mysql引擎创建数据库

CREATE DATABASE IF NOT EXISTS jlc_product
ENGINE = MySQL('host:port', ['database' | database], 'user', 'password')


CREATE DATABASE IF NOT EXISTS snb_live
ENGINE = MySQL('host:port', ['database' | database], 'user', 'password')

show databases


SELECT userId AS user_id,
       'JLC' as biz,
       'premium' as series,
       'invest' as dim,
       SUM(toFloat32OrZero(transAmount)) AS amount
FROM jlc_product.recharge_record
WHERE payResult = 'SUCCESS'
GROUP BY userId
having amount <> 0 limit 10

SELECT userId AS user_id,
       'JLC' as biz,
       'premium' as series,
       'invest' as dim,
       transAmount AS amount
FROM jlc_product.recharge_record
WHERE payResult = 'SUCCESS' limit 10



select userId as user_id, 'JLC' as biz, 'premium' as series,'invest' as dim, transamount as amount FROM jlc_product.recharge_record limit 10

SELECT user_id,
        case when product_type = 1 then 'SNB' else 'MCB' end biz,
       'APP' as series,
       'total_amount' as dim,
       toFloat32OrZero(total_amount) as amount
FROM snb_live.plan_portfolio_account limit 10


select part_log_day, count(*) 
from user_trade_fact.user_amount_fact group by part_log_day


CREATE TABLE IF NOT EXISTS dim_common_external.dim_date_day
(
  `date_id` String,
  `datestr_id` String,
  `day_of_month` UInt8,
  `month_num` UInt8,
  `month_name` String,
  `month_name_cn` String,
  `year_month_id` String,
  `month_first_date` String,
  `month_last_date` String,
  `quarter_id` UInt8,
  `quarter_first_date` String,
  `quarter_last_date` String,
  `year_id` String,
  `day_of_week` UInt8,
  `week_of_year` UInt8
) ENGINE = MergeTree()

create database dim_common_external