---
title: trojan的使用
tag: ["trojan"]
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover1.jpg
---
trojan一个可以提供代理功能的网络工具。
<!--more-->
除了trojan，类似的工具还有ShadowSocks、SSH等。SSH使用动态转发实现`（ssh -N -D 127.0.0.1:1088 test@52.221.60.138 -p997`。

## 服务端
### 安装

使用下面脚本可自动安装最新版本安装，并添加为系统服务，一些系统的软件仓库也有提供，但不一定是最新版的。也可以在[这里](https://github.com/trojan-gfw/trojan/releases)下载使用。

```shell
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/trojan-gfw/trojan-quickstart/master/trojan-quickstart.sh)"
```

完成后可看到如下信息：

```
Unpacking trojan 1.16.0...
Installing trojan 1.16.0 to /usr/local/bin/trojan...
Installing trojan server config to /usr/local/etc/trojan/config.json...
Installing trojan systemd service to /etc/systemd/system/trojan.service...
Reloading systemd daemon...
```

trojan的版本是1.16.0，安装位置在`/usr/local/bin/trojan`，默认配置文件位置`/usr/local/etc/trojan/config.json`，和添加trojan为系统服务的配置文件位置`/etc/systemd/system/trojan.service`。

### 配置服务端

安装好后，会生成一个模版配置文件`/usr/local/etc/trojan/config.json`，使用时可以根据需要修改部分内容（建议先备份一下）。下面几个参数比较重要，可根据需要修改。详细参数说明参考这里：[Config](https://trojan-gfw.github.io/trojan/config)

`run_type`：有`"server" | "client" | "forward" | "nat"`四个可选项，这里服务端使用默认的`"server"`
`local_addr`: 服务器地址，默认`0.0.0.0`即可，如需使用IPv6需要改为`::`.；
`local_port`：trojan服务端口，默认443，如无特殊需求不建议使用其他端口；
`remote_addr`和`remote_port`：非trojan协议时，将请求转发处理的地址和端口。可以是任意有效的ip/域名和端口号，默认是本机和80端口；
`password`：密码，多个密码分行填写，最后一行不需要逗号；
`cert`和`key`：域名的SSL证书和密钥的位置，cert最好填好fullchain证书的位置。

注意配置文件的语法不用有错误，否则启动服务会出错。

据前述，`cert`和`key`填写SSL证书的路径，证书的申请可以使用acme.sh或certbot等ACME客户端。如Let's Encrypt的证书通常是3个月需要更新，证书更新后需要重启服务端是更新生效。可以使用crontab设置定时任务来自动更新证书，重启trojan服务；对于`remote_addr`和`remote_port`，一个简单的方案是`remote_addr`填写一个已有的网站，当非trojan协议访问时跳转到该网站，使用默认值`127.0.0.1`使其跳转到本机`remote_addr`的HTTP服务，当然这需要在本机搭建一个HTTP服务。

### 启动、停止服务

`trojan -h`查看trojan的使用：

```
trojan [-htv] [-l LOG] [-k KEYLOG] [[-c] CONFIG]
options:
  -c [ --config ] CONFIG 指定配置文件
  -h [ --help ]          显示帮助信息
  -k [ --keylog ] KEYLOG specify keylog file location (OpenSSL >= 1.1.1)
  -l [ --log ] LOG       指定log文件位置
  -t [ --test ]          测试配置文件
  -v [ --version ]       显示版本等信息
```

安装并修改好默认配置文件后可直接使用`trojan`命令启动服务端，如果要使用其他配置文件可使用`-c /path/for/config`参数指定其位置。

按前述方法安装好程序后，同时自动将`trojan`添加到系统服务，如果是手动下载软件包使用的，可仿照下面内容编辑配置文件添加系统服务，文件名可为`trojan.service`，可存储到`/etc/systemd/system/`。

```
[Unit]
Description=trojan
Documentation=https://trojan-gfw.github.io/trojan/config https://trojan-gfw.github.io/trojan/
After=network.target network-online.target nss-lookup.target mysql.service mariadb.service mysqld.service

[Service]
Type=simple
StandardError=journal
ExecStart="/usr/local/bin/trojan" "/usr/local/etc/trojan/config.json"
ExecReload=/bin/kill -HUP $MAINPID
LimitNOFILE=51200
Restart=on-failure
RestartSec=1s

[Install]
WantedBy=multi-user.target
```

添加好系统服务后，如果需要开机自启，执行`sudo systemctl enable trojan`即可。

### 用户认证与流量控制

trojan除了使用配置文件的密码认证外，还可以使用MySQL (MariaDB) 数据库，在trojan配置文件有`"mysql"`块，当`"enable"`为`true`时启用数据库，填写数据库地址等信息。`"key"`、`"cert"`、`"ca"`用于配置CA文件（可选）。

```json
"mysql": {
    "enabled": true,
    "server_addr": "127.0.0.1",
    "server_port": 3306,
    "database": "trojan",
    "username": "trojan",
    "password": "",
    "key": "",
    "cert": "",
    "ca": ""
}
```

数据库需要有`users`表，如下：

```sql
CREATE TABLE users (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL,
    password CHAR(56) NOT NULL,
    quota BIGINT NOT NULL DEFAULT 0,
    download BIGINT UNSIGNED NOT NULL DEFAULT 0,
    upload BIGINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    INDEX (password)
);
```

其中，`password`, `quota`, `download`,  `upload`字段是必须的，`download`记录下载流量值，`upload`记录上传流量值，`quota`为阈值，`download + upload < quota`允许连接，`quota`为负值表示不限流量。

### 示例

示例中在浏览器访问域名强制使用HTTPS。流量示意图如下，图中绿线是合法的trojan流量，可进行代理访问；而红色的是非trojan流量，将转向web服务，如HTTPS访问直接转向1999端口的web服务，而若使用HTTP访问则转向443端口，再转向1999端口实现强制HTTPS访问。trojan服务监听443端口，Nginx或Caddy服务监听80和1999端口。如果不需要强制HTTPS，也可以在80端口运行web服务，非trojan流量转发到80端口，如右侧所示。

![waYazF.png](https://s1.ax1x.com/2020/09/12/waYazF.png)
具体配置的，在trojan配置文件中`remote_addr`和`remote_port`使用以下设置：

```json
"remote_addr": "127.0.0.1",
"remote_port": 1999
```

Ubuntu下，在`/etc/nginx/sites-available/`目录创建一个`my.domain.com`文件，使用以下配置：

```ini
# 访问80端口的流量转发到443
server {
    listen 127.0.0.1:80 default_server;
    server_name my.domain.com;
    location / {
        proxy_pass https://my.domain.com;
    }
}
# 将使用IP访问的流量转发到https即443端口
server {
    listen 0.0.0.0:80;
    listen [::]:80;
    server_name 0.0.0.0;
    location / {
        return 301 https://my.domain.com$request_uri;
    }
    location /.well-known/acme-challenge {
       root /var/www/acme-challenge;
    }
}
# 运行在1999端口的web服务
server {
    listen 0.0.0.0:1999;
    listen [::]:1999;

    server_name _;
    location / {
        root /var/www/html;
    }
}
```

删除`/etc/nginx/sites-enabled/`目录下的`default`文件，创建一个`my.domain.com`软链到到此目录：

```shell
ln -s ln -s /etc/nginx/sites-available/my.domain.com /etc/nginx/sites-available/
```

重启Nginx服务即可`sudo systemctl restart nginx`。

这样，就可以使用trojan客户端，来使用代理功能，而使用浏览器访问`my.domain.com`时则会打开web页面。

使用Caddy实现与上面相同的效果，其配置文件：

```
:80 {
    redir https://my.domain.com{uri} 301
}
:1999 {
    encode zstd gzip
    templates
    root * ./test
    file_server browse
}
```



## 客户端

trojan自身集成有简单的客户端，另外其他支持trojan协议的客户端都可以使用。如[clash](https://github.com/Dreamacro/clash)、[V2Ray-Desktop](https://github.com/Dr-Incognito/V2Ray-Desktop)（Linux、mac）[igniter](https://github.com/trojan-gfw/igniter)（Android）、Shadowrocket（IOS）等。

### trojan

使用trojan原生客户端仅监听SOCKS5端口，如果需要浏览器使用需要**设置系统代理**或在浏览器安装[SwitchyOmega](https://github.com/FelisCatus/SwitchyOmega)插件配合使用。

客户端安装、使用方法与服务端相同，区别在与配置文件，使用时只需要把`remote_addr`改为服务器地址（域名）、`remote_port`修改与服务器配置相同（通常为443），`password`填写服务器验证密码，`local_port`可根据需要修改。

```json
{
    "run_type": "client",
    "local_addr": "127.0.0.1",
    "local_port": 1080,
    "remote_addr": "example.com",
    "remote_port": 443,
    "password": [
        "password1"
    ],
    "log_level": 1,
    "ssl": {
        "verify": true,
        "verify_hostname": true,
        "cert": "",
        "cipher": "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:AES128-SHA:AES256-SHA:DES-CBC3-SHA",
        "cipher_tls13": "TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384",
        "sni": "",
        "alpn": [
            "h2",
            "http/1.1"
        ],
        "reuse_session": true,
        "session_ticket": false,
        "curves": ""
    },
    "tcp": {
        "no_delay": true,
        "keep_alive": true,
        "reuse_port": false,
        "fast_open": false,
        "fast_open_qlen": 20
    }
}
```

Linux使用也按服务器配置方法设置为系统服务并设置开机自启。

---

**参考**

1. [trojan教程 - tlanyan](https://tlanyan.me/trojan-tutorial/#intro)
2. [trojan-tutor.github.io](https://trojan-tutor.github.io/2019/04/10/p41.html)
3. [trojan-gfw.github.io](https://trojan-gfw.github.io/trojan/)
4. [自建梯子教程 --Trojan版本](https://trojan-tutor.github.io/2019/04/10/p41.html)