---
title: Ubuntu远程连接-Xrdp
tag: ['tag1','tag2']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover2.jpg
---

abstract

<!--more-->

之前在Red Hat系统上使用VNC作为远程连接工具，体验还算可以，后来在Deepin以及Ubuntu上也尝试使用VNC，但是不知是配置的原因还是其他什么原因，使用体验不是很好，而且经常不能正常显示，了解到Xrdp这一工具后，在Ubuntu20上安装使用，发现还不错，至少不用怎么配置就可以正常显示。

## Xrdp安装使用

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

## 可能遇到的一些问题

### 需要权限认证 
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

### 缺失Dock栏
安装gnome-tweaks(gnome-tweak-tool)，打开Tweaks在Extensions选项卡中开启appindicators换dock扩展即可。
![Nmxrwt.png](https://s1.ax1x.com/2020/06/18/Nmxrwt.png)

---

**参考**
1. [Azure: Installing GNOME desktop and xRDP to access an Ubuntu 17.10 Server - TechKB.onl]( https://www.techkb.onl/azure-installing-gnome-desktop-and-xrdp-to-access-an-ubuntu-1710-server/)
