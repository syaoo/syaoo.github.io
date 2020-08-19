---
title: RIME-linux中文输入法安装使用
tag: ['输入法','RIME']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover0.jpg
---

RIME／中州韵输入法引擎，是一个跨平台的输入法算法框架。

<!--more-->
CentOS 8 安装
在安装过程中如遇到某些库缺失的情况可根据提示查找，安装
1. librimels

2. 
CentOS 8 软件仓库找不到该软件，所有从[github](https://github.com/rime/ibus-rime)下载源码安装。

根据说明文档给出的依赖需求安装所需软件:
y
>build dependencies:
>
>- pkg-config
>- cmake>=2.8
>- librime>=1.0 (development package)
>- libibus-1.0 (development package)
>- libnotify (development package)
>- plum (submodule)
>
>runtime dependencies:
>- ibus
>- librime>=1.0
>- libibus-1.0
>- libnotify
>- rime-data (provided by plum)

cmake  gcc-c++ pkgconf-pkg-config.x86_64
```
warning: ibus-rime-1.4.0-3.fc32.x86_64.rpm: Header V3 RSA/SHA256 Signature, key ID 12c944d0: NOKEY
error: Failed dependencies:
	brise >= 0.35 is needed by ibus-rime-1.4.0-3.fc32.x86_64
	librime.so.1()(64bit) is needed by ibus-rime-1.4.0-3.fc32.x86_64
```

---

**参考**
1. [title](url)
