# cmdb

```mermaid
graph LR
域名 --> 云解析
云解析 --> 线路

线路 --> 主机
线路 --> CDN
线路 --> OSS
线路 --> SLB监听
线路 --> 站点

CDN --> OSS
CDN --> 站点
CDN --> 云解析
CDN --> SLB监听

站点 --> Location
站点 --> OSS

Location --> 站点
Location --> 云解析
Location --> 服务监听
Location --> OSS

SLB监听 --> 服务监听

服务监听 --> 中间件服务
服务监听 --> 业务程序


服务 --> 服务监听
服务 --> 云解析

中间件服务 --> 主机
业务程序 --> 主机
```

## 添加数据

```graphql
# 添加Host数据
mutation addHost($host: [AddHostInput!]!) {
  addHost(input: $host) {
    host {
      id
      name
      ip
    }
  }
}

# gqlvariables
{
  "host": {
    "ip": "10.103.27.177",
    "name": "jenkins"
  }
}

```

## 修改数据

```graphql
mutation updateHost($host: UpdateHostInput!) {
  updateHost(input: $host){
    host {
      id
      name
      ip
    }
  }
}

# gqlvariables

{
  "host": {
    "filter": {
      "ip": {"alloftext": "10.103.27"}
    },
    "set": {
      "name": "jenkins177-base-prod-ds"
    }
  }
}

```

## 查询数据

```graphql
query queryHost {
  queryHost(filter: { name: { anyoftext: "base" } }) {
    id
    name
    ip
  }
}
```
