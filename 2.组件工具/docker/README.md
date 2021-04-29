# docker 知识汇总梳理

## docker构建过程

### ONBUILD 命令

> ONBUILD `<cmd>` 当前镜像最为基础镜像构建时执行。

### 多阶段构建

> COPY --FROM=0 `<source image/source file>` `<target>`
> COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf

### ARG 构建参数

> ARG <参数名>[=<默认值>]

## docker运行过程

### 数据卷

> docker volume create `<name>`
> docker volume ls
> docker volume inspect `<name>`
> docker volume prune 清除无主的数据卷

### 挂载数据卷

> docker run -d -P --name `<name>` --mount source=`<vol-name>`, target=`<target-name>`
> docker run -d -P --name `<name>` --mount type=bind,source=`<vol-name>`, target=`<target-name>`,readonly

### 给容器一个固定IP地址

```bash
# 新建一个网络
docker network create -d bridge --subnet 172.25.0.0/16 <net-name>
# 容器启动，指定网络
docker run -network=<net-name> -ip=172.25.3.3 -itd --name=<container> <image-name>
```
