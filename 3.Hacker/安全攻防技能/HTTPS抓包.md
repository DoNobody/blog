[首页](/)
# 常规用burpsuite或者fiddler

## chrome浏览器HSTS强校验问题

在使用抓包软件抓取https网站时，很多时候网站的response header中会添加`Strict-Transport-Security: max-age=172800`,
使用这个header后，浏览器会记录正在使用的证书，并且在接下来的172800秒内，如果证书有变动则触发HSTS安全策略。

这是一个`浏览器` 的安全策略，所以可以在chrome中进行配置。

在Chrome浏览器中输入：`chrome://net-internals/#hsts`,就可进行配置。

**删除校验**
> 1、`Query HSTS/PKP domain：` 中 搜索要删除的网站：www.baidu.com

```bash
Found:
static_sts_domain:
static_upgrade_mode: UNKNOWN
static_sts_include_subdomains:
static_sts_observed:
static_pkp_domain:
static_pkp_include_subdomains:
static_pkp_observed:
static_spki_hashes:
dynamic_sts_domain: www.baidu.com
dynamic_upgrade_mode: FORCE_HTTPS
dynamic_sts_include_subdomains: false
dynamic_sts_observed: 1593436786.545947
dynamic_sts_expiry: 1593609586.545943
```

> 2、`Delete domain security policies：` 中删除网站：www.baidu.com

## 使用SSL Pinning技术防止中间人攻击

[Certificate and Public Key Pinning](https://owasp.org/www-community/controls/Certificate_and_Public_Key_Pinning)

**可以参考的工具**

```URL
https://github.com/datatheorem/TrustKit-Android
https://github.com/datatheorem/TrustKit
```
