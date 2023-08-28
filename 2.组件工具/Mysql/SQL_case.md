[首页](/)
# 一些经典、常用的SQL语句

## mysq1 下分组排序取组内前几

```sql
SELECT rk1,
       nick_name,
       order_day,
       nums,
       amt1,
       amt2
FROM
  (SELECT t1.*,
          if(@o_day=t1.order_day,@rank:=@rank+1,@rank:=1) AS rk1,@o_day:=t1.order_day
   FROM
     (SELECT u.nick_name,
             a.*
      FROM
        (SELECT user_id,
                date_format(order_time,"%Y-%m-%d") order_day,
                count(DISTINCT order_id) nums,
                sum(estimate_cos_price) amt1,
                sum(estimate_fee) amt2
         FROM order_goods
         WHERE order_state IN (2,
                               3,
                               4)
           AND user_id <> -1
         GROUP BY order_day,
                  user_id) a
      LEFT JOIN `user` u ON a.user_id = u.id
      ORDER BY a.order_day DESC,a.nums DESC) t1,

     (SELECT @o_day :=NULL,@rank:=0) r) RESULT
```

## 分组连续最大活跃天数

```sql
--  mysql下
SELECT user_id,
       max(nums) times
FROM
  (SELECT user_id,
          c_day,
          count(c_day) nums
   FROM
     (SELECT user_id,
             a_day,
             rk1,
             date_sub(a_day,INTERVAL rk1 DAY) c_day
      FROM
        (SELECT a.user_id,
                a.a_day,
                if(@o_user_id=a.user_id,@rank:=@rank+1,@rank:=1) AS rk1, @o_user_id:=a.user_id AS tmp
         FROM
           (SELECT user_id,
                   date(appear_log_day) AS a_day
            FROM biz_appear
            WHERE appear_log_day > '2021-01-01'
            GROUP BY user_id,
                     date(appear_log_day)
            ORDER BY user_id,
                     a_day) a
         JOIN
           (SELECT @o_user_id :=NULL, @rank :=0) r) t) t1
   GROUP BY user_id,
            c_day) t2
GROUP BY user_id
ORDER BY times DESC


-- clickhouse 下
select
  user_id,
  max(c_nums) c_days
from
  (
  select
    user_id,
    c_day,
    count(c_day) c_nums
  from
    (
    select
      user_id,
      a_day,
      r1,
      datesub(a_day,
      r1) c_day
    from
      (
      select
        user_id,
        groupArray(appear_log_day) a_day,
        arrayEnumerate(a_day) AS r1
      from
        (
        select
          user_id,
          date(stime) appear_log_day
        from
          markpoint.fact_markpoint_ysh fmy
        where
          stime > '2021-04-01'
          and user_id > '0000000'
          and user_id < '99999999999'
        group by
          user_id,
          date(stime)
        order by
          user_id,
          date(stime))
      group by
        user_id)
array
    join a_day,
      r1)
  group by
    user_id,
    c_day)
group by
  user_id
```
