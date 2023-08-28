[首页](/)
# Windows 下有用命令

## netsh window下进行端口转发

```shell
# 查看已有有的端口转发
netsh interface portproxy show all

# 添加端口转发
netsh interface portproxy add v4tov4 listenport=80 connectaddress=127.0.0.1 connectport=30080

# 删除短裤转发
netsh interface portproxy delete v4tov4 listenport=443 listenaddress=127.0.0.1

```
