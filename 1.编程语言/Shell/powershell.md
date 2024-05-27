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
## 查看文件属性，并修改文件属性
```shell
# 查看文件现在属性
 Get-ItemProperty -Path .\DESKTOP-4BQGCC0-20240527-1003.log|Format-list -Property * -Force

# 修改文件特定属性
Set-ItemProperty -Path .\DESKTOP-4BQGCC0-20240527-1003.log -Name LastWriteTime -Value '2024-05-01 12:00:00'
```
