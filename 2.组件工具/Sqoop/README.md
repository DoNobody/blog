# sqoop ETL工具

* 一次导入多个表

```shell
cat table_list.txt | xargs -i sqoop-import --connect jdbc:mysql://127.0.0.1:3306/database?useCursorFetch=true\&dontTrackOpenResources=true\&defaultFetchSize=2000\&autoReconnect=true\&connectTimeout=3000\&socketTimeout=600000 --username username --password password --hive-database user_database --hive-overwrite -m 1 --create-hive-table --hive-import --table {}
```

* 导入数据库中所有表

```shell
sqoop-import-all-tables --connect jdbc:mysql://127.0.0.1:13008/user_database?useCursorFetch=true\&dontTrackOpenResources=true\&defaultFetchSize=2000\&autoReconnect=true\&connectTimeout=3000\&socketTimeout=600000 --username username --password password --hive-database hive_databases --hive-overwrite -m 1 --create-hive-table --hive-import
```
