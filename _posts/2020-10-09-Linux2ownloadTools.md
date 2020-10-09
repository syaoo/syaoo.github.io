---
title: linuxdow
tag: ['tag1','tag2']
mathjax: false
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---

abstract

<!--more-->
在Linux系统中最常用的两个CLI下载工具是`wget`和`curl`，初次之外还有其他许多有用的下载工具、甚至是torrents下载工具。

## Wget

这是一款功能丰富且非常有名的下载工具，除基本的下载功能外，还具有恢复下载、多文件下载、下载带宽管理等功能。下面介绍`wget`的常用的下载功能，`wget -h`可查看其更多使用帮助。

1. 下载文件

   ```shell
   # 下载html文件
   wget https://linux.cn/article-7369-1.html
   # 下载html文件并保存为a.html
   wget https://linux.cn/article-7369-1.html -O a.html
   ```

2. 后台下载

   ```shell
   # 后台下载文件
   wget -b https://linux.cn/article-7369-1.html 
   # 后台下载文件，保存文件名为a.html同时把log信息保存到downloadlog_a.log
   wget -b https://linux.cn/article-7369-1.html -O a.html -o downloadlog_a.log
   ```

3. 端点续传

   ```shell
   # 文件下载意外中断后可使用-c参数继续下载文件
   wget -c https://linux.cn/article-7369-1.html -O a.html
   ```

4. FTP下载

   ```shell
   # 从FTP下载文件
   # wget --ftp-user=<user_name> --ftp-password=<Give_password> Download-url-address 
   ```

## Curl

## Axel


---

**参考**

1. [Linux 下十大命令行下载工具](https://linux.cn/article-7369-1.html)
