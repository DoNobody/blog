# 一些经典、常用的SQL语句

## sql

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
