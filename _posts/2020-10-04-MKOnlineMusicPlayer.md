---
title: MKOnlineMusicPlayer
tag: ['web']
article_header:
mathjax: false
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover0.jpg
---

一款开源在线音乐播放器。

<!--more-->
[MKOnlineMusicPlayer](https://github.com/mengkunsoft/MKOnlineMusicPlayer)是一款开源的基于 [Meting](https://github.com/metowolf/Meting) 的在线音乐播放器。具有音乐搜索、播放、下载、歌词同步显示、个人网易云音乐播放列表同步等功能。从Github下载源文件，然后配置好环境即可通过浏览器访问使用。

## 配置运行环境

### PHP环境

在使用该播放器前需要在服务器安装PHP环境：`sudo dnf install php php-json`，CentOS安装php时默认没有安装json模块，需要额外安装`php-json`。可以使用`php -v`查看php版本，修改`/etc/php.ini`可以更改php配置，启动PHP FastCGI管理器:`sudo systemctl start php-fpm.service`，设置开机自启：`sudo systemctl enable php-fpm.service`。

### Web服务器

PHP安装好后，安装配置Web服务器如Apache、Nginx、Caddy等，文中使用Caddy作为Web服务器。从[Github](https://github.com/caddyserver/caddy/releases)发布页下载对应的文件，解压后即可运行caddy。[更多方式](https://caddyserver.com/docs/download)安装。Caddyfile（文件名为Caddyfile）参考如下内容配置：

```yaml
domain.com {
    root * /path/for/MKOnlineMusicPlayer
    file_server
    php_fastcgi unix//run/php-fpm/www.sock
    log {
        output file /var/log/caddy/example.com.access.log {
                roll_size 3MiB
                roll_keep 5
                roll_keep_for 48h
        }
        format console
    }
    # 使用自定义证书；可忽略
    tls /path/for/fullchain.pem /paht/for/key.pem
}
```
编辑好Caddyfile即可启发Caddy，`sudo caddy run -config Caddyfile`，即可访问播放器。

## 播放器设置
`MKOnlineMusicPlayer`目录下，`api.php`文件可以对对播放器做一定配置如：启动HTTPS、启用DEBUG、设置网易云COOKIE等。如遇不能正常获取播放列表时，可以启用DEBUG，查看是否缺失某些模块。访问`mydomain.com\api.php`，确保所有服务器函数检查状态都为可用。

`js/player.js`文件可以自定义播放列表。

---

**参考**

1. [How to Install and Configure Caddy Web Server with PHP and MariaDB on Ubuntu 20.04](https://www.howtoforge.com/tutorial/ubuntu-caddy-web-server-installation/)

