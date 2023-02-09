# K8S

## k8s 日常命令

### k8s 删除 namespace terminated

```shell
# 查看ns
kubectl.exe get ns
# 导出terminated ns 配置
kubectl.exe get ns kuboard -o json > kuboard-delete.json
# 编辑删除 spec.finalizers 下的配置
vim kuboard-delete.json
# 单独启动 k8s proxy 8081 
kubectl.exe proxy --port=8081

# 使用 修改后的配置文件
curl -k -H "Content-Type:application/json" -X PUT --data-binary @kuboard-delete.json http://127.0.0.1:8081/api/v1/namespaces/kuboard/finalize
# 查看确定删除
kubectl.exe get ns
```
