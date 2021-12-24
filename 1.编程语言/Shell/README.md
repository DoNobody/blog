# Shell 的日常

## 常用命令

```shell
# shell中进行boolean值的比较
bool=true
if [ "$bool" = true ]; then
elif [ "$bool" = "true" ]; then
elif [[ "$bool" = true ]]; then
elif [[ "$bool" = "true" ]]; then
elif [[ "$bool" == true ]]; then
elif [[ "$bool" == "true" ]]; then
elif test "$bool" = true; then
elif test "$bool" = "true"; then
    echo "Test shell boolean"
fi
```

```shell
# AWK 的一个case
find . -mindepth 2 -name "*.md" | awk -F'/' 'BEGIN {RS=".md"} {k=$3;v=$2"/"$3"/"$4;if ($4=="README") {k=$3;v=$2"/"$3"/"} else if ($4=="") {k=$3;v=$2"/"$3} else k=$3"_"$4;arr[$2]=arr[$2]"\n  - ["k"]("v")"} END { num = asorti(arr, indices); for (i=1; i<=num; ++i) if (indices[i]) print "- "indices[i], arr[indices[i]]}'
```

```shell
# 替换主机IP到shadowsocks.json中
#!/bin/bash

eth0ip=`ip a|grep "/18"|awk '{print $2}'|awk -F'/' '{print $1}'`
sed -i "s/\(\"server\"\:\"\).*\(\",\)/\1$eth0ip\2/g" /etc/shadowsocks.json
/usr/local/bin/ssserver -c /etc/shadowsocks.json -d start
```
