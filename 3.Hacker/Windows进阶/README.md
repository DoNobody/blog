# 记录Windows下的日常

## Chocolatey 包管理工具

> 这是基于.NET Framework 4以上的windows安装软件的命令行工具

### 安装

```text
第一步，打开你的powershell.exe，使用管理员方式运行
第二步，运行命令 Get-ExecutionPolicy
    如果返回 Restricted ，那么运行Set-ExecutionPolicy AllSigned 或者 Set-ExecutionPolicy Bypass -Scope Process
第三步，运行命令 Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

### 命令使用

```Text
运行 choco 测试chocolatey是否安装成功
升级Chocolatey，运行 choco upgrade chocolatey
```
