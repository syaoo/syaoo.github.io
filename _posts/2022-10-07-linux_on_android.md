---
title: 在Android运行Linux的几种方法
date: 2022-09-30 16:20
tag: ['linux','Android']
mathjax: false
mathjax_autoNumber: true
# Mermaid
mermaid: false
# Chart
chart: false
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover0.jpg
---

体验了目前已知的三种在Android上安装linux的方法：Linux Deploy、Termux、Aidlux。
<!--more-->
- Linux Deploy需要root使用具有一定门槛，系统安装方便，功能扩展性更强，可以使用低位端口号、管理手机硬件等。
- Termux无需root、使用方便、即开即用、默认没有图形界面、具有较强扩展性。Termux安装的gcc其实clang，不过似乎也可以通过一些方法安装gcc。
- Aidlux无需root、使用简单、默认具有图像界面，但是安装体积较大，且对系统版本和设备的性能有一定要求。

## Linux Deploy

[Linux Deploy](https://github.com/meefik/linuxdeploy/releases)需要使用ROOT权限，使用Magisk可以获取并管理ROOT权限。使用方法可以参考下面其中一篇内容：
- [Android 玩家必备神器入门：从零开始安装 Magisk - 少数派](https://sspai.com/post/67932)
- [Installation - Magisk](https://topjohnwu.github.io/Magisk/install.html)
- [Magisk安装教程 - Magisk中文网](https://magiskcn.com/)

Linux Deploy的使用也比较简单，打开软件后主界面写着简单的使用引导。首先点击右下角配置安装选项（下图左侧），如发行版、安装类型、用户名、密码、是否启用ssh等，具体各项说明可参考[Linux Deploy 指南](https://zixijian.github.io/2020/09/01/007.html)。注意配置安装选项时一定要启用ssh，否则可能在安装好后无法连接系统。配置完成后点击右上角菜单中的安装，待安装完成后再点击下方的启动按钮即可通过ssh连接已安装的系统。

![Linux Deploy](/pic/linux_on_android/ld010.jpg)

### 自动启动服务
右下角打开设置，勾选初始化启用，SSH连接到linux，新建/etc/rc.local目录，在其中添加启动脚本，启动脚本需要至少包含以下内容
```shell
case "$1" in
  start)
    # 系统启动过程中执行的命令
    ;;
  stop)
    # 系统关闭过程中执行的命令
    ;;
esac
```
```shell
#! /bin/bash

### BEGIN INIT INFO
# Description:       Run Foo service
### END INIT INFO

USER=android
BASE_DIR=/home/android/program/alist
echo $0
start_with_nohup(){
        echo "Start Alist Server..."
        cd $BASE_DIR
        su ${USER} -c 'nohup ./alist server > /dev/null 2>&1 &'
        echo "Start Alist Server ok"
}
start_with_screen(){
        echo "Start Alist Server..."
        #sudo -u ${USER} /bin/bash -c 'cd $HOME/program/alist && screen -dmS alist ./alist server'
        cd $BASE_DIR
        # sudo -u ${USER} /bin/bash -c 'screen -dmS alist ./alist server'
        sudo -u ${USER} screen -dmS alist ./alist server
        echo "Start Alist Server ok"
}
case "$1" in
  start)
          start_with_nohup
          #start_with_screen
    ;;
  stop)
    echo "Stopping Alist Server..."
    #sudo -u ${USER} bash -c 'pkill -ef "dmS alist ./alist server"'
    sudo -u ${USER}  pkill -ef "alist server"
    sleep 2
    ;;
  *)
    echo "Usage: /etc/init.d/foo {start|stop}"
    exit 1
    ;;
esac

exit 0
```

### 断网
使用linux deploy的chroot方案安装了debian之后出现这个问题的原因主要是安卓的doze mode，在termux下键入su 进入类似adb shell的模式，然后使用dumpsys deviceidle disable禁用这个锁屏之后的睡眠模式。

[解决安卓linux dploy下非root用户的进程在锁屏几分钟之后断网的问题--禁用doze mode。](https://blog.csdn.net/fjh1997/article/details/111207694)
[开机自动挂载Linux Deploy中的Linux容器并开启adbd网络调试 | Torrk's Blog](https://conimi.com/archives/127/#_0x40-%E5%88%86%E6%9E%90init-rc)
## Termux

[Termux](https://github.com/termux/termux-app/releases)是一个Android终端模拟器和Linux环境APP，其不需要root即可实现在Android上使用Linux环境。Termux自身具有最新化的Linux基础系统环境，而且可以使用包管理器(pkg/apt)来安装其他软件，如openssh实现通过ssh方法Termux。

![termux](/pic/linux_on_android/termux01.jpg)

### 通过ssh连接Termux

在Termux按以下安装、启动ssh服务，即可在另一台设备上通过ssh登陆Termux，Termux中ssh server默认使用的端口是8022.

```sh
# 安装OpenSSH
pkg install openssh

# 启动SSH Server
sshd

# 获取用户名
whoami

# 获取IP
ifconfig

#设置密码
passwd 
```

连接ssh

```sh
ssh user@ip -p 8022
```

通过[PRoot](https://wiki.termux.com/wiki/PRoot)可以实现在Termux内安装其他各种发行版本的Linux系统，同时Termux提供[proot-distro](https://github.com/termux/proot-distro)工具可以方便快捷的安装Arch、Debian、Alpine等多种Linux系统。

### 在Terminal内安装ArchLinx

1. 使用pkg安装proot-distro

```sh
pkg install proot-distro
```

2. 查看proot-distro支持的Linux系统列表
![proot-distro list](/pic/linux_on_android/termux-proot3.png)

3. 安装archlinux
![proot-distro install](/pic/linux_on_android/termux-proot2.png)

4. 进入archlinux
![proot-distro login](/pic/linux_on_android/termux-proot4.png)


在使用`proot-distro install`安装系统时如遇到`CANNOT LINK EXECUTABLE "curl": library "libssl.so.1.1" not found`，可尝试使用pkg update更新程序。

## Aidlux

Aidlux是阿里开发的智能物联网开发平台，通过它可以在Android手机上使用Linux，该软件不需要Root，在各家应用商店均可直接下载安装。当前1.2.1内置的是一个完整的Debian 10，可以开箱即用，同时还自带图形界面，界面应该是以web方式实现的，其中文件管理器的后台是filebrowser，一个web文件管理器。

![aidlux手机端截图](/pic/linux_on_android/aidlux00.jpg)

在aidlux中点击Cloud_ip会启动web远程桌面，通过其中提供的地址可以在浏览器中使用aidlux。

![aidlux远程桌面截图](/pic/linux_on_android/aidlux03.png)

---

1. [Termux和Linux Deploy的性能测试 - 知乎](https://zhuanlan.zhihu.com/p/162121013)
2. [android - What are the differences between Termux, PRoot, Userland, Linux Deploy, AnLinux and Alpine? - Super User](https://superuser.com/questions/1546024/what-are-the-differences-between-termux-proot-userland-linux-deploy-anlinux)
3. [GitHub - meefik/linuxdeploy: Install and run GNU/Linux on Android](https://github.com/meefik/linuxdeploy)
4. [极致安卓之—Termux安装完整版Linux - 知乎](https://zhuanlan.zhihu.com/p/95865982)
6. [小米10 MIUI 12 Magisk root教程（无需刷REC） - 知乎](https://zhuanlan.zhihu.com/p/338754547)
7. [PRoot - Termux Wiki](https://wiki.termux.com/wiki/PRoot)
8. [Linux Deploy 指南](https://zixijian.github.io/2020/09/01/007.html)