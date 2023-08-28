[首页](/)
# Nginx

## ModSecurity

>[ModSecurity误拦截处理方法](http://www.modsecurity.cn/practice/post/6.html)

```shell
# 使用modsecurity 添加白名单
# 特定主机名，移除特定种类的 检查规则
SecRule REQUEST_HEADERS:Host "@pm dms-7cA3hI8zwy.example.com" \
     "id:10000,phase:1,pass,nolog,ctl:ruleRemoveByTag=attack-sqli"

```
