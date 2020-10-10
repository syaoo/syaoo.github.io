---
title: Linux中的几款下载工具
tag: ['Linux']
mathjax: false
# dadsa
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---

介绍了几款Linux系统中的下载工具常用的wget、curl等，媒体下载工具youtube-dl、you-get以及几种Torrent下载工具。

<!--more-->
在Linux系统中最常用的两个CLI下载工具是`wget`和`curl`，初次之外还有其他许多有用的下载工具、甚至是torrents下载工具。

## 基础下载工具
### Wget

这是一款功能丰富且非常有名的下载工具，除基本的下载功能外，还具有恢复下载、多文件下载、下载带宽管理等功能。下面介绍`wget`的常用的下载功能，`wget -h`可查看其更多使用帮助。
```shell
# 下载html文件
wget https://linux.cn/article-7369-1.html
# 下载html文件并保存为a.html
wget https://linux.cn/article-7369-1.html -O a.html

# 后台下载文件
wget -b https://linux.cn/article-7369-1.html 
# 后台下载文件，保存文件名为a.html同时把log信息保存到downloadlog_a.log
wget -b https://linux.cn/article-7369-1.html -O a.html -o downloadlog_a.log

# 断点续传，文件下载意外中断后可使用-c参数继续下载文件
wget -c https://linux.cn/article-7369-1.html -O a.html

# 从FTP下载文件
wget --ftp-user=<user_name> --ftp-password=<Give_password> Download-url-address 
```

###  Curl

Curl是另一款Linux上常用的下载工具，与wget类似同样支持多文件下载、断点续传等功能。
```shell
# 从文件地址下载文件并存为um.mp4
curl -o um.mp4 http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4
# 以原始文件件名保存文件
curl -O http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4 

curl -O http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_2mb.mp4 -O http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4
```

### Aria2、Axel

aria2是一种开源命令行下载加速器，支持多个端口，你可以使用最大带宽来下载文件，其支持Linux、win等多平台。axel也是一款加速下载器，可同时下载多个文件片段以提高下载速度。aria2的功能更为丰富，许多下载工具如Motrix都是基于aria2开发的。

```shell
# 安装aria2
sudo apt install aria2
# 下载文件
aria2c http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4 
# 安装axel
sudo apt install axel
# 下载文件
axel http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4
```

## 视频下载工具

### Youtube-dl

[youtube-dl](https://ytdl-org.github.io/youtube-dl/index.html)是一款跨平台的视频下载工具，从名字可知其能够下载YouTube的视频，当然也支持其他[许多网站](https://github.com/ytdl-org/youtube-dl/tree/master/youtube_dl/extractor)的音视频下载；[这里](https://github.com/ytdl-org/youtube-dl/blob/master/README.md#installation)有介绍各平台的安装方式，下面是Linux上的安装方法：

```shell
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl
# 使用pip安装
pip install youtube_dl
```

视频下载

```shell
# B站视频下载, 可以-o参数指定下载文件的名称
youtube-dl https://www.bilibili.com/video/BV1ii4y1j7ZE
# 使用代理下载YouTube视频
youtube-dl --proxy socks5://127.0.0.1:1099 "https://www.youtube.com/watch?v=4x678Pwpk6A"
```

### You-Get

[you-get](https://github.com/soimort/you-get)与youtube-dl基本类似，不过似乎对国内网站的支持要更好。支持网站[列表](https://you-get.org/#supported-sites)。[安装](https://github.com/soimort/you-get#installation)也比较方便:

```shell
pip3 install you-get
```

视频下载：

```shell
# 下载腾讯视频
you-get https://v.qq.com/x/page/a0864n9sxrx.html
# 使用socks5代理下载视频，需要PySocks库
you-get -s 127.0.0.1:1099 "https://www.youtube.com/watch?v=4x678Pwpk6A"
# 下载网易云音乐歌曲
you-get https://music.163.com/#/song?id=486999661
```
**[Movgrab](https://github.com/ColumPaget/Movgrab)**也是一款网络视频下载工具，只是好久没有更新了。

## Torrent下载工具
Linux的Torrent下载工具有[rtorrent](https://github.com/rakshasa/rtorrent)、ctorrent、[Transmission](https://transmissionbt.com/)等。

---

**参考**

1. [Linux 下十大命令行下载工具](https://linux.cn/article-7369-1.html)
