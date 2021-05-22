---
title: SAMBA配置及使用
tag: ['samba']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover0.jpg
---


使用Samba配置文件共享服务器，通过windows、linux、Android等系统访问文件服务器。

<!--more-->

## 服务端设置（Linux）

1. 安装samba
   `sudo apt install samba `
   
2. 配置 
   smb的配置文件在`/etc/samba/smb.conf`内容分两部分`global`和`share`，前者为全局设置，后者当前共享目录设置。下面是一个share配置的示例`[]`中的字符`pub`是共享目录显示的名称，其中关键的字段`path`用于指定共享目录路径。

   ```bash
   [pub]
       comment = some comment
       path = /mnt/netdisk/pub
       valid users = samba
       public = yes
       read only = no
       create mask = 0700
       directory mask = 0700
       available = yes
       browseable = yes
       display charset = UTF-8
       unix charset = UTF-8
       dos charset = cp936
   
   ```

   详细配置介绍参加[Samba服务器搭建与配置 | 曹世宏的博客](https://cshihong.github.io/2018/10/18/Samba%E6%9C%8D%E5%8A%A1%E5%99%A8%E6%90%AD%E5%BB%BA%E4%B8%8E%E9%85%8D%E7%BD%AE/)

3. 用户管理
   
   ```bash
   # 添加用户 添加的用户必须是系统用户
   smbpasswd -a [username]
   # 或者
   pdbedit -a [username]
   # 修改密码
   smbpasswd [username]
   # 删除用户
   pdbedit –x [username]
   #或
   smbpasswd –x [username]
   # 其他
   pdbedit –L #列出Samba用户列表，读取passdb.tdb数据库文件。
   pdbedit –Lv #列出Samba用户列表详细信息。
   ```


## 连接服务器

### Windows

`win+R`打开运行，输入`\\`+samba服务器的地址（IP或域名）:`\\192.168.1.1`，根据提示输入用户名、密码即可进入共享目录。

#### 连接失败
遇到“您不能访问此共享文件夹，因为你组织的安全策略阻止未经身份验证的来宾访问，这些策略可帮助保护你的电脑免受网络上不安全不安全和设备或恶意设备的威胁”提示，无法连接smb服务。找到四种解方案：

1. 在`smb.conf`文件中移除/注释 `map to guest = bad user` 或 设置 `map to guest = never`；
2. 修改注册表，`Ctrl+r`输入`regedit`进入注册表编辑器，找到`计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters`将`AllowInsecureGuestAuth`值修改为`1`;
3. 修改组策略，`计算机配置`-`管理模版`-`网络`-`Lanman工作站`-`启用不安全的来宾登陆`，编辑策略设置，改为“已启用”。

### Android & IOS

Android下需要使用samba客户端或者具有samba功能的文件管理器，Android端推荐使用[**CX文件管理器**](https://play.google.com/store/apps/details?id=com.cxinventor.file.explorer)：除本地文件管理外，还支持网盘（DropBox、GoogleDrive、OneDrive、box）、SMB、FTP、WebDAV等。IOS端推荐使用**ES文件浏览器**。

![](https://lh3.googleusercontent.com/CzB_9p-ngt9NHwkiGo_hdGXSUCYVwTKmdnzAdkgIKdXNmc7OeEbs2NY4gRtBkOK_XOs=w1728-h1080-rw)

### Linux

在linux有两种方法连接，一使用smbclient，二是借助cifs挂载。

### 使用smbclient连接

1. 列出主机下的共享文件夹

   ``` bash
   smbclient -L 198.168.0.1 -U username%password
   ```

2. 用类似FTP的方式连接smb服务器

   ```bash
   smbclient //192.168.0.1/tmp  -U username%password
   ```

   进入smbclient环境后，可以进行类似FTP的操作，通过如cd 、lcd、get、megt、put、mput等命令，可以访问远程主机的共享资源。

### 挂载目录

1. 创建挂载点

   ```bash
   mkdir sharedir
   ```

2. 挂载目录

   ```bash
   sudo mount -t cifs -o user=<username>,password=<password>,uid=<user>,gid=<group>  /host/share ./sharedir/
   ```

   注意要加上`uid`和`gid`参数使指定到用户和用户组具有相应到访问权限。

3. `df`可用查看挂载情况。


**参考**
1. [smbclient 命令，Linux smbclient 命令详解：交互方式访问samba服务器 - Linux 命令搜索引擎](https://wangchujiang.com/linux-command/c/smbclient.html)
2. [[SOLVED] W10: You can't access this shared folder because your organization's security policies block unauthenticated guest access - General Support - Unraid](https://forums.unraid.net/topic/59672-solved-w10-you-cant-access-this-shared-folder-because-your-organizations-security-policies-block-unauthenticated-guest-access/)
3. [Windows 10 不能访问Samba共享 "因为你组织的安全策略阻止未经身份验证的来宾访问" - 简书](https://www.jianshu.com/p/be7dc5875923)
4. [你不能访问此共享文件夹，因为你组织的安全策略阻止未经身份验证的来宾访问...](https://social.technet.microsoft.com/Forums/zh-CN/6ea3bfd7-582a-4333-a932-594a5a5394d8?forum=win10itprogeneralCN)
