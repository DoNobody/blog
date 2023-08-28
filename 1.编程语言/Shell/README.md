[首页](/)
# Shell 的日常

## 常用命令

### shell中进行boolean值的比较

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

### AWK 的一个case

```shell

find . -mindepth 2 -name "*.md" | awk -F'/' 'BEGIN {RS=".md"} {k=$3;v=$2"/"$3"/"$4;if ($4=="README") {k=$3;v=$2"/"$3"/"} else if ($4=="") {k=$3;v=$2"/"$3} else k=$3"_"$4;arr[$2]=arr[$2]"\n  - ["k"]("v")"} END { num = asorti(arr, indices); for (i=1; i<=num; ++i) if (indices[i]) print "- "indices[i], arr[indices[i]]}'
```

### 替换主机IP到shadowsocks.json中

```shell
#!/bin/bash
# python -m pip install https://github.com/shadowsocks/shadowsocks/archive/master.zip -U
eth0ip=`ip a|grep "/18"|awk '{print $2}'|awk -F'/' '{print $1}'`
sed -i "s/\(\"server\"\:\"\).*\(\",\)/\1$eth0ip\2/g" /etc/shadowsocks.json
/usr/local/bin/ssserver -c /etc/shadowsocks.json -d start
```

### shell 统计Nginx  log并发送邮件

```shell
#!/bin/bash

DATA1=`date -d '1 days ago' +%d/%b/%Y`
DATA2=`date +%Y%m%d`

FILE1='api.example.com-https.log'
TO='manager1@example.com manager2@example.com'
echo "URL MaxTime AveTime TotalRequests" > ${FILE1}_url_groupby.log &&
zcat /server/logs/nginx/$FILE1-$DATA2.gz|grep "$DATA1"|sed 's/\xA0/ /g'|tr -d '['|tr -d ']'|awk '{print $10,$6}'|awk -F"?" '{print $1}'|awk '{m[$2]=m[$2]>$1?m[$2]:$1;s[$2]+=$1;c[$2]+=1}END{ for(i in s){print i,m[i],s[i]/c[i],c[i]} }'|sort -k3 -r -n >> ${FILE1}_url_groupby.log  &&
echo "<html>" > email.html
echo "<Body>" >> email.html
awk 'BEGIN{print "<table border=\"1\">"} {print "<tr>";for(i=1;i<=NF;i++)print "<td>" $i"</td>";print "</tr>"} END{print "</table>"}' ${FILE1}_url_groupby.log  >> email.html
echo "</Body>" >> email.html
echo "</html>" >> email.html

sendEmail -o tls=yes -f auto@example.com -t ${TO} -s smtp.exmail.qq.com:587 -xu auto@example.com -xp password -u "hostname01_$FILE1-$DATA1" -o message-content-type=html -m "`cat email.html`"
```
