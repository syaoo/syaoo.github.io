---
title: Linux挂载webdav网盘
tag: ['linux', 'webdav']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover1.jpg
---
简单介绍在Linux中挂载使用WebDav网盘的方法。

<!--more-->

<!-- # Linux挂载webdav网盘 -->

## 1. 安装davfs2 

挂载WebDav首先需要安装davfs2，在debian系中可以使用apt命令安装

```sh
sudo apt install davfs2
```

安装过程中会提示是否允许非管理员用户挂载webdav，可根据需要选择。后期也可以使用`sudo dpkg-reconfigure davfs2`重新修改设置。

webdav网盘的挂载有多种方式，例如使用mount命令、利用fstab挂载，还有利用systemd挂载。本文仅涉及两种方式。

## 2. 使用mount命令手动挂载

无论那种挂载方式都需要有一个挂载点，例如可以新建一个`/mnt/dav`文件夹作为挂载点

```bash
mkdir /mnt/dav
```

使用mount命令挂载网盘，其中用`-t`参数设置挂载文件系统类型为davfs，`https://webdav.example/path`是webdav的地址。根据提示输入账户、密码即可完成挂载。

```bash
sudo mount -t davfs https://webdav.example/path /mnt/dav
```

这里需要使用管理员权限完成，虽然已经将用户添加到davfs2用户组，并且重新登陆用户或使用`newgrp - davfs2`切换用户组，也是不行会提示：`must be superuser to use mount.`。

## 3. 使用fstab挂载

利用fstab配置可以实现普通用户挂载或者开机自动挂载webdav网盘。

### 3.1 普通用户手动挂载

首先需要将指定用户添加到davfs2用户组

```sh
 sudo usermod -aG davfs2 username
```

在`/etc/fstab`中添加如下行，其中`uid`和`gid`用于指定挂载后文件所属用和用户组，`noauto`表示使用`mount -a`命令不会挂载该设备，`_netdev`表示该设置挂载需要依赖网络。然后普通用户可以使用`mount /mnt/dav`命令即可挂载，其中`/mnt/dav`就是`/etc/fstab`中设置的挂载点。

```
https://webdav.example/path /mnt/dav davfs rw,user,uid=username,gid=username,noauto,_netdev 0 0 
```

这里使用`mount`挂载时依然会要求输入用户名密码，可以在`/etc/davfs2/secrets`或`~/.davfs2/secrets`按照如下格式添加地址、用户名和密码，然后将文件的读写权限设置为600。之后用户挂载时便不需要输入密码。`/etc/davfs2/secrets`中的设置对所有用户有效，`~/.davfs2/secrets`仅对当前用户有效。

```sh
touch ~/.davfs2/secrets
echo "https://webdav.example/path davusername davpassword" >> ~/.davfs2/secrets
chmod 600 ~/.davfs2/secrets
```

### 3.2 自动挂载

如果有在设备启动时自动挂载的需要，可以在`/etc/fstab`的配置中添加`x-systemd.automount`，如下配置`x-systemd.device-timeout=10`等待相应时间为10s。

```
https://webdav.example/path /mnt/dav davfs rw,user,uid=username,gid=username,noauto,x-systemd.automount,x-systemd.device-timeout=10,_netdev 0 0 
```

使用自动挂载时一定需要在`/etc/davfs2/secrets`中添加地址、用户名和密码，并将文件权限值设置为600

```sh
echo "https://webdav.example/path davusername davpassword" | sudo tee -a /etc/davfs2/secrets
sudo chmod 600 /etc/davfs2/secrets
```

这里不能再使用mount命令挂载，需要使用`systemctl restart mnt-dav.automount`命令，其中服务名称`mnt-dav.automount`由`/etc/fstab`中设置的挂载地址`/mnt/dav`构成。

```sh
sudo systemctl daemon-reload # 修改fstab后需要使用
sudo systemctl restart mnt-dav.automount
```

解除挂载使用如下命令
```sh
sudo systemctl stop home-xw-dav.automount
```

---

1. [davfs2 - ArchWiki](https://wiki.archlinux.org/title/Davfs2)
2. [How To Install ownCloud 7 On Ubuntu 14.04](https://www.howtoforge.com/how-to-install-owncloud-7-on-ubuntu-14.04)
3. [Mounting a WebDAV directory in Linux (Ubuntu)](https://techiech.blogspot.com/2013/04/mounting-webdav-directory-in-linux.html)
4. [Fstab - Use SystemD automount - Manjaro](https://wiki.manjaro.org/index.php/Fstab_-_Use_SystemD_automount)
5. [fstab - ArchWiki](https://wiki.archlinux.org/title/fstab)