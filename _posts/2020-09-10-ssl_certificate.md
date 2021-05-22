---
title: SSL证书申请与配置acme.sh和certbot
tag: ["ssl", "certbot", "acme.sh"]
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover1.jpg
---

使用acme.sh、certbot申请SSL证书，以gossa文件服务器（Nginx）和Jupyter服务为例。
<!--more-->

Let‘s Encrypt支持通配符证书，使用acme.sh或certbot申请时必须同时指定主域名，如:

```shell
acme.sh --issue  -d my.domain.com -d *.domain.com   --nginx 
sudo certbot certonly --standalone -d my.domain.com -d *.domain.com
```


## acme.sh

acme.sh是使用shell脚本编写的一个acme客户端，可以方便的申请Let's Encrpty等SSL证书。
安装直接使用下面的命令即可（普通用户或root用户均可）：
```
curl  https://get.acme.sh | sh
```
acme.sh会安装到用户目录下，`.acme.sh`内， 并创建了一个bash alias, `alias acme.sh=~/.acme.sh/acme.sh`，使用`source`命令更新或重启Terminal即可直接使用`acme.sh`命令。
acme.sh的使用可以参考[说明 · acmesh-official/acme.sh Wiki](https://github.com/acmesh-official/acme.sh/wiki/%E8%AF%B4%E6%98%8E)
使用`--standalone`参数或主机上无运行在80端口的web服务器时，需要安装`socat`才可以。
由于Let's Encrypt对域名申请证书分次数有一定限制，在测试的时候使用`--test`参数可以有效避免因短时间内申请次数过多而失败。

### 使用acme.sh为gossa服务添加https

[gossa](https://github.com/pldubouilh/gossa)是一个简洁轻巧的开源web文件服务器，借助[caddy](https://caddyserver.com/)可以实现用户认证及HTTPS功能，[配置方法](https://github.com/pldubouilh/gossa/tree/master/support#multi-account-setup)也很简单。在本示例中使用Nginx实现端口转发及HTTPS。

这里使用acme.sh生成证书，acme.sh的基本使用也比较简单。通常Nginx的证书可以使用下面的命令直接生成（HTTP验证方式）：

```shell
acme.sh --issue  -d my.domain.com   --nginx
```
不过该方法对于无公网IP（无法从公网访问）的主机是行不通的，所以acme.sh提供了DNS验证方式。DNS验证有手动和API自动验证的两种方式。acme.sh目前支持 cloudflare, dnspod, cloudxns, godaddy 以及 ovh 等数十种解析商的API，不同服务商的使用方式略有不同，具体可以参考这里：[How to use DNS APIi](https://github.com/acmesh-official/acme.sh/wiki/dnsapi)。文中是使用阿里云的API来产生证书。

##### 使用DNS API验证域名
###### 设置API key和secret
首先需要登陆阿里云，到**AccessKey 管理**（在用户头像处有该入口）创建AccessKey。虽然不是必须，为了保证安全推荐创建子账户来创建AccessKey，在创建AccessKey时系统也会提示使用这一安全机制。
AccessKey创建好后，记录key和secret（**注意不要泄露！！！**），然后再Terminal设置`Ali_Key`和`Ali_Secret`变量。

```shell
export Ali_Key="dafadfadfejaj"
export Ali_Secret="dasfadfafjasdfja"
```

##### 生成证书
使用下面的命令生成Nginx的证书
```shell
# 对于阿里云 --dns的参数是dns_ali
acme.sh --issue --dns dns_ali  -d my.domain.com
# 泛域名
acme.sh --issue --dns dns_ali  -d domain.com -d *.domain.com
```
    完成后会给出证书的位置:
```shell
[Thu Sep 10 03:38:21 EDT 2020] Your cert is in  /home/user/.acme.sh/my.domain.com/my.domain.com.cer 
[Thu Sep 10 03:38:21 EDT 2020] Your cert key is in  /home/user/.acme.sh/my.domain.com/my.domain.com.key 
[Thu Sep 10 03:38:21 EDT 2020] The intermediate CA cert is in  /home/user/.acme.sh/my.domain.com/ca.cer 
[Thu Sep 10 03:38:21 EDT 2020] And the full chain certs is there:  /home/user/.acme.sh/my.domain.com/fullchain.cer 
```
文件说明：
- ca.cer：Let’s Encrypt的中级证书
- fullchain.cer：包含中级证书的域名证书
- my.domain.com.cer：无中级证书的域名证书
- my.domain.com.conf：该域名的配置文件
- my.domain.com.csr：该域名的CSR证书请求文件
- my.domain.com.csr.conf：该域名的CSR请求文件的配置文件
- my.domain.com.key：该域名证书的私钥

##### 证书安装
把证书文件复制到Nginx配置文件指定的位置即可，acme.sh提供`--install-cert`命令可供安装证书：

```shell
acme.sh --install-cert -d example.com \
--key-file       /path/to/keyfile/in/nginx/key.pem  \
--fullchain-file /path/to/fullchain/nginx/cert.pem \
--reloadcmd     "service nginx force-reload"
```

`--reloadcmd`参数`"service nginx force-reload"`让Nginx服务器重新加载证书。Nginx 的配置 `ssl_certificate` 使用 `fullchain.cer` ，而非 `<domain>.cer` ，否则 [SSL Labs](https://www.ssllabs.com/ssltest/) 的测试会报 `Chain issues Incomplete` 错误。

##### 证书更新
目前，acme.sh会在60天后自动更新证书，由于acme 协议和 letsencrypt CA 都在频繁的更新，可以使用`acme.sh  --upgrade  --auto-upgrade`开启acme.sh自动升级，减少自动更新出错的可能。acme.sh的自动更新是一颗`crontab`实现的，每天 0:00 点自动检测所有的证书, 如果快过期了, 需要更新, 则会自动更新证书。
当然，也可以使用在到期前需要更新的话可以使用`--force`和`--renow`参数强制更新。

##### 撤销与手动更新证书

```shell
acme.sh --renew -f -d my.domain.com --dns dns_ali # 强制更新证书，当证书到期时间多余30天时使用-f
acme.sh --revoke -d my.domain.com # 撤销证书
```

#### Nginx端口转发配置

简单配置Nginx的即可实现端口转发，直接使用域名来访问文件服务器，而不需要加端口号，并且将http的80端口转向https的443端口。配置如下：

```yaml
 server {
     listen       443 ssl;
     listen       [::]:443 ssl;
     server_name  my.domain.com;
     # 配置ssl证书路径及其他设置
     ssl_certificate            /home/user/SSL/my.domain.com/fullchain.pem; # 证书
     ssl_certificate_key        /home/user/SSL/my.domain.com/key.pem; # 证书key
     ssl_session_cache shared:SSL:1m;
     ssl_session_timeout  10m;
     ssl_ciphers PROFILE=SYSTEM;
     ssl_ciphers PROFILE=SYSTEM;
     ssl_prefer_server_ciphers on;
     
     # 需要转发的服务
     location / {
         proxy_pass http://127.0.0.1:8001;
     }

     error_page 404 /404.html;
     location = /40x.html {
     }

     error_page 500 502 503 504 /50x.html;
         location = /50x.html {
     }
 }
server {
    listen       80;
    server_name  my.domain.com;
    # 将http重定向到https
    rewrite ^(.*)$ https://$http_host$1 permanent;
    # 如果使用IP或其他域名访问重定向到https://my.domain.com
    if ($host != 'my.domain.com') {
       rewrite ^(.*) https://my.domain.com$request_uri? permanent;
}
```

上面是基本配置，还可以参考有关资料做进一步优化，其中关键部分做了注释说明。将上面的内容填入到配置文件（CentOS下在`/etc/nginx/nginx.conf`）的对应位置即可。

配置好后重启服务器即可生效，需要注意的是，当证书不存在或路径错误时会启动失败。另外在CentOS上，由于443端口默认没有打开，要确保443端口开放，其他设备才能访问。

```shell
firewall-cmd --list-ports 查看已开放端口
sudo firewall-cmd  --zone=public --add-port=443/tcp --permanent # 开放443端口
sudo firewall-cmd --reload # 重启防火墙使设置生效
```

## certbot

certbot是Let‘s Encrypt官方推荐的一款ACME客户端，功能、使用与acme.sh类似，
安装certbot，可以从系统软件仓库安装，也可以使用pip安装，这里选择后者。

```shell
pip3 install certbot certbot-dns-aliyun
```
cerbot有许多插件可以根据需要按装，如`python3-certbot-nginx`、`python3-certbot-apache`分别用于自动为Nginx、Apache服务器自动配置证书。`cerbot-dns-aliyun`是阿里云的DNS插件，其他DNS服务商也需要相应的插件，官方支持[列表](https://certbot.eff.org/docs/using.html#dns-plugins)。

[这里](https://certbot.eff.org/instructions)有针对不同系统及web服务的使用指导，更详细说明可以参考[官方文档](https://certbot.eff.org/docs/using.html)。

### 使用certbot申请证书并为Jupyterlab配置HTTPS

这里同样使用DNS API的域名验证方式，首先需要从DNS服务商申请API，这里使用阿里云，为安全起见阿里云的RAM功能创建子账号，并授权与`AliyunDNSFullAccess`权限，仅用于域名解析的设置，生成AccessKey，小心保存。

#### 配置认证文件

创建一个DNS API的认证文件`aliyun.ini`,分别把其中的`dns_aliyun_access_key`和`dns_aliyun_access_key_secret`的值替换为之前保存的`AccessKey ID`和`AccessKey Secret`：

```ini
dns_aliyun_access_key = LTAI4GJS8v5Ma123dfadT
dns_aliyun_access_key_secret = RWdawJmq0h17352Kda23s7QBEsd6rSD
```

#### 申请证书

使用下面的命令来申请证书：

```shell
certbot certonly -a dns-aliyun\
--dns-aliyun-credentials certbot/aliyu.ini \
-d my.domain.com \
--work-dir certbot/work/ \
--logs-dir certbot/logs/ \
--config-dir certbot/config/ --test-cert
```

`-a dns-aliyun`指定使用的阿里云API，``--dns-aliyun-credentials`指定之前创建的认证文件，`--test-cert`参数是用于测试证书申请，可避免申请次数超限。

第一次使用是会要求输入一个邮箱，用于提醒更新证书或接收其他信息。

```
Enter email address (used for urgent renewal and security notices)
 (Enter 'c' to cancel): 
```

之后按提示，同意服务条款、选择是否接收证书服务商的新闻（广告）邮件。等待申请完成即可。成功申请后会有一段输出“IMPORTANT NOTES:”，说明了证书的存放位置及到期时间等信息。

由于没有Jupyter没有自动安装插件，还需要把正式复制到Jupyter配置文件指定的位置。

#### 配置Jupyter

修改配置文件`~/.jupyter/jupyter_notebook_config.py`中如下字段的值，保存后重启服务即可。

```bash
# Path to the certificate 
c.NotebookApp.certfile = '/etc/letsencrypt/live/example.com/fullchain.pem' 
# Path to the certificate key we generated
c.NotebookApp.keyfile = '/etc/letsencrypt/live/example.com/privkey.pem' 
```

#### 更新撤销证书

当密钥丢失或其他一些原因需要吊销证书是可以使用：

```bash
certbot revoke --cert-path /etc/letsencrypt/live/my.domain.com/fullchain.pem # 吊销证书
certbot delete --cert-name example.com # 删除相关文件
```

`certbot renew`可用于更新证书，同时也可以使用‘hooks’指定需要运行的命令或脚本

```shell
# 更新证书前停止nginx，更新完成后重启nginx
certbot renew --pre-hook "service nginx stop" --post-hook "service nginx start"
```

自动更新，官方推荐使用cronjob的方式（与acme.sh类似），如，每天0点12点执行检查是否需要更新。

```shell
echo "0 0,12 * * * root python3 -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew -q --pre-hook 'service haproxy stop' --post-hook 'service haproxy start'" | sudo tee -a /etc/crontab > /dev/null
```

Github Action 部署 acme.sh 全自动批量签发多域名证书 https://www.ioiox.com/archives/104.html

---

**参考**

1. [使用acme.sh与阿里云DNS签发Let’s Encrypt的免费数字证书](https://ngx.hk/2019/01/27/%E4%BD%BF%E7%94%A8acme-sh%E4%B8%8E%E9%98%BF%E9%87%8C%E4%BA%91dns%E7%AD%BE%E5%8F%91lets-encrypt%E7%9A%84%E5%85%8D%E8%B4%B9%E6%95%B0%E5%AD%97%E8%AF%81%E4%B9%A6.html)
2. [说明 · acmesh-official/acme.sh Wiki](https://github.com/acmesh-official/acme.sh/wiki/%E8%AF%B4%E6%98%8E6)
3. [Linux 下使用 acme.sh 配置 Let's Encrypt 免费 SSL 证书 + 通配符证书 - 烧饼博客](https://sb.sb/blog/linux-acme-sh-lets-encrypt-ssl/)
4. [Certbot 申请 LetsEncrypt 泛域名免费证书 - IT DevOps Club](https://www.fandenggui.com/post/certbot-dns-aliyun-letsencrypt.html)
5. [Welcome to certbot-dns-cloudflare’s documentation! — certbot-dns-cloudflare 0 documentation](https://certbot-dns-cloudflare.readthedocs.io/en/stable/)
6. [User Guide — Certbot 1.8.0.dev0 documentation](https://certbot.eff.org/docs/using.html#dns-plugins)

