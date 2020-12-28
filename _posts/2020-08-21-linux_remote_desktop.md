---
title: Linux远程桌面-XRDP
tag: ['xrdp']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover2.jpg
---

Linux有多种远程桌面连接方式，大致可以分为vnc和rdp两种，vnc类的服务端有tigervncserver，x11vnc等，rdp类的服务端有xrdp。这三种都可以实现远程桌面功能，通过直接vnc/rdp协议的客户端，可以轻松连接远程桌面。根据我的使用经验，xrdp与x11vnc安装使用都比较方便，出现的问题较少，也容易解决，而tigervncserver则可能会出现如黑屏、灰屏等奇奇怪怪的问题。就使用效果来看，xrdp远程或本地只能有一个登陆桌面，否则后登陆的那个不能进入桌面；tigervncserver有点类似虚拟桌面的感觉，远程和本地可以同时登陆，且二者独立显示内容，同时登陆是有些软件不能同时打开，如firefox浏览器；x11vnc远程本地是同步的，二者是操作的同一个桌面。
<!--more-->

## xrdp
我在Ubuntu 20 及Deepin 20都有测试使用xrdp，使用效果都不错。

###  安装
直接在Terminal使用apt命令安装：
```bash
sudo apt install -y xrdp
```
安装完成后即可直接使用。在参考文章[1]中提到，普通用户不能直接连接，需要修改`/etc/X11/Xwrapper.config`中的`allowed_users=console`为`allowed_users=anybody`才可以连接。可以使用下面的命令修改：
```bash
sudo sed -i 's/allowed_users=console/allowed_users=anybody/' /etc/X11/Xwrapper.config
```
### 远程连接
在win上可以直接使用系统自带的“远程桌面连接”工具，打开远程桌面连接输入服务器地址，成功连接后输入用户名，密码即可进入远程桌面。
![NmjW4S.png](https://s1.ax1x.com/2020/06/18/NmjW4S.png)

在Linux系统，如Ubuntu可以使用Remmina选择RDP连接。

### 可能遇到的一些问题

####  需要权限认证 
使用过程中如果经常弹出权限认证（Authentication Required），可是在`/etc/polkit-1/localauthority.conf.d/`目录下创建一个名为`02-allow-colord.conf1`的文件，并写入以下内容：
```bash
polkit.addRule(function(action, subject) {
if ((action.id == "org.freedesktop.color-manager.create-device" ||
action.id == "org.freedesktop.color-manager.create-profile" ||
action.id == "org.freedesktop.color-manager.delete-device" ||
action.id == "org.freedesktop.color-manager.delete-profile" ||
action.id == "org.freedesktop.color-manager.modify-device" ||
action.id == "org.freedesktop.color-manager.modify-profile") &&
subject.isInGroup("{group}")) {
return polkit.Result.YES;
}
});
```

####  缺失Dock栏
安装gnome-tweaks(gnome-tweak-tool)，打开Tweaks在Extensions选项卡中开启appindicators换dock扩展即可。
![Nmxrwt.png](https://s1.ax1x.com/2020/06/18/Nmxrwt.png)




---

**参考**
1. [Azure: Installing GNOME desktop and xRDP to access an Ubuntu 17.10 Server - TechKB.onl]( https://www.techkb.onl/azure-installing-gnome-desktop-and-xrdp-to-access-an-ubuntu-1710-server/)
