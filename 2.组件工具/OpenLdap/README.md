# 修改 openldap 的用户权限控制

```shell
dn: olcDatabase={1}mdb,cn=config
changetype: modify
delete: olcAccess
-
add: olcAccess
olcAccess: {0}to * by dn.exact=gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth manage by * break
olcAccess: {1}to attrs=userPassword,shadowLastChange by self write by dn="cn=admin,dc=example,dc=com" write by anonymous auth by * none
olcAccess: {3}to dn.subtree="ou=DevOps1,ou=Depts,dc=example,dc=com" by dn="cn=Manager,dc=example,dc=com" read
olcAccess: {4}to dn.subtree="ou=Groups,dc=example,dc=com" by dn="cn=Manager,dc=example,dc=com" read
olcAccess: {5}to dn.subtree="dc=example,dc=com" by dn="cn=Manager,dc=example,dc=com" search
olcAccess: {6}to * by self read by dn="cn=admin,dc=example,dc=com" write by dn="cn=readonly,dc=example,dc=com" read
olcAccess: {100}to * by * none
```

> 在 ou=Groups 下的组 objectClass 添加 simpleSecurityObject 类型用于登录验证

```shell
objectClass=["groupOfUniqueNames", "simpleSecurityObject"]
```

> 根据组用户来访问包含用户信息，用作权限管理

```shell
# 能访问ou=People节点
# 能访问ou=Groups下的所有组信息
# 配置ou=Groups下的组只能访问包含的用户
dn: olcDatabase={1}mdb,cn=config
changetype: modify
delete: olcAccess
-
add: olcAccess
olcAccess: {0}to * by dn.exact=gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth manage by * break
olcAccess: {1}to attrs=userPassword,shadowLastChange by self write by dn=cn=admin,dc=example,dc=com write by anonymous auth by * none
olcAccess: {3}to dn.exact=ou=People,dc=example,dc=com by dn.children=ou=Groups,dc=example,dc=com read by * break
olcAccess: {4}to dn.subtree=ou=Groups,dc=example,dc=com by dn.children=ou=Groups,dc=example,dc=com read by * break
olcAccess: {5}to dn.subtree=dc=example,dc=com by set="this/memberOf & user" read by dn.children=ou=Groups,dc=example,dc=com search by * break
olcAccess: {6}to * by self read by dn=cn=admin,dc=example,dc=com write by dn=cn=readonly,dc=example,dc=com read by * none
```

## 配置 openldap 的 accesslog

> [参考文章](https://www.npcglib.org/~stathis/blog/2020/11/20/enable-access-logs-for-an-openldap-database/)
> Enable the AccessLog Module

```shell
dn: cn=module{2},cn=config
objectClass: olcModuleList
cn: module{2}
olcModuleLoad: {0}accesslog.so
# osixia/docker-openldap 中
olcModulePath: /usr/lib/ldap/
```

> Create an AccessLog database

```shell
dn: olcDatabase={2}mdb,cn=config
objectClass: olcDatabaseConfig
objectClass: olcMdbConfig
olcDatabase: mdb
olcDbMaxSize: 85899345920
olcDbDirectory: /var/lib/ldap/accesslog
olcSuffix: cn=accesslog
olcRootDN: cn=admin,cn=accesslog
olcRootPW: auditor_password
olcDbIndex: default eq
olcDbIndex: entryCSN,objectClass,reqEnd,reqResult,reqErr,reqStart
```

> Add the AccessLog overlay to the “source” database

```shell
dn: olcOverlay=accesslog,olcDatabase={1}mdb,cn=config
objectClass: olcOverlayConfig
objectClass: olcAccessLogConfig
olcOverlay: accesslog
olcAccessLogDB: cn=accesslog
olcAccessLogOps: all
olcAccessLogSuccess: TRUE
# scan the accesslog DB every day, and purge entries older than 30 days
olcAccessLogPurge: 07+00:00 01+00:00
```
