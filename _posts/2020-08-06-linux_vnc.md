---
title: VNC的安装与使用
tag: ['vnc']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover2.jpg
---

新版的Tigervnc（>=1.10.0）不再支持vncserver命令启动远程桌面服务。取而代之的是通过systemed作为系统服务的方式来启动。旧版tigervncserver与其他vnc服务端使用方法类似，通过vncserver命令启动，通常需要配置xstartup文件使远程桌面可正常显示。另外x11vnc也是另一可选vnc服务端。对比x11vnc和tigervncserver（旧版），发现前者远程登陆与本地登陆桌面使用的是同一个环境（进程），就是远程与本地的操作是同步可见的；而后者tigervncserver，本地与远程各自使用不同桌面环境，远程和本地操作互不可见。

<!--more-->
最近升级CentOS 8中的软件后发现，`vncserver`命令不能用了，无论怎样都输出

```
vncserver has been replaced by a systemd unit.
Please read /usr/share/doc/tigervnc/HOWTO.md for more information.
```
仔细阅读了HOWTO.md发现是Tigervnc改变了启动方式，`vncserver`命令被废弃了。

## Tigervnc server(>=1.10.0)启动方式
新版TigerVNC使用systemd方式启动服务，可以方便的设置开机自己，配置简单，目前在Ubuntu18、Ubuntu20和CentOS 8上使用都很顺利，没有出现使用旧版时的玄学问题。目前唯一不爽的是vnc服务开启时，该用户不能本地登陆，输入密码后黑屏。
### 添加用户映射

在`/etc/tigervnc/vncserver.users`文件中可以添加用户映射用于指定用户使用的vnc端口，按如下格式，`x`表示用户使用的端口，`user`表示用户名：
```
:x=user
```
如，用户test1和test2分别使用端口5901和5902：
```
:1=test1
:2=test2
```
### 配置Xvnc
在`/etc/tigervnc`目录下的`vncserver-config-defaults`是Xvnc的默认配置文件，对所有用户有效。用户也在`$HOME/.vnc/config`中指定自己的配置。另外`/etc/tigervnc`目录下的`vncserver-config-mandatory`可以做全局配置，此文件中的设置具有最高优先级，会覆盖`vncserver-config-defaults`中及用户的设置。
设置方式：
```
option=value
option
```
示例：
```
session=gnome
securitytypes=vncauth,tlsvnc
desktop=sandbox
geometry=2000x1200
localhost
alwaysshared
```
**注意**：`session`选项必须设置，且必须与目录`/usr/share/xsessions`下的桌面session同名。如Ubuntu中，需要设置为
```
session=ubuntu
```

### 设置VNC密码
启动服务前必须为每个用户设置密码，否则会启动失败。使用`vncpasswd`命令按提示设置即可。
**注意**：如果使用过以前版本的Tigervnc用户目录下可能存在`.vnc/passwd`文件，需要删除重新使用`vncpasswd`生成，或者使用下面的命令更新：
```
restorecon -RFv /home/<USER>/.vnc
```
### 启动Tigervcn服务

使用下面命令即可启动`x`端口的vnc服务（将`x`替换为前面设置的端口号）。
```
sudo systemctl start vncserver@:x
```
将vnc服务设置为开机自启：
```
sudo systemctl enable vncserver@:x
```
**注意**：如果以前将Tigervnc设置为系统服务，需要删除相应的配置，以确保新的系统服务配置可以正常使用。

新版Tigervnc可以更方便的以系统服务的方式启动vnc服务，并设置开机自启，而且经过在CentOS 8和Ubuntu 20、Ubuntu 18的测试发现，不在需要xstartup配置文件，服务启动即可正常连接显示远程桌面。但也有一些不足，如当用户已使用图形界面登陆时不能开启该用户的vnc服务，且vnc服务开启后，用户将不能在本地登陆，这点类似xrdp，不知道未来是否会改变。

其他的启动方法可以参考[这里](https://wiki.archlinux.org/index.php/TigerVNC#Installation)

## 使用x11vnc作为服务端

之前使用的都是tigervnc之类的作为服务端但是总是不能很顺利的安装使用，同样的配置在不同的设备可能会有不同的效果，虽然使用xrdp可以很方便的安装使用，但是xrdp有一个问题是，如果使用远程登陆桌面，本地就不能在登陆桌面，反之已然，这有时造成一些不便。
最近发现x11vnc作为服务端似乎可以很顺利的安装使用，这次是在Deepin20上测试的，效果不错：
```bash
# 1. 安装x11vnc
sudo apt install x11vnc
# 2. 密码设置
x11vnc -storepasswd
# 3. 启动服务器
x11vnc -rfbport 5900 -rfbauth ~/.vnc/passwd -display :0 -forever -bg -repeat -nowf -o ~/.vnc/x11vnc.log
```
### 启动失败解决方法
如果启动失败，log文件有如下提示：
```
** If NO ONE is logged into an X session yet, but there is a greeter login
   program like "gdm", "kdm", "xdm", or "dtlogin" running, you will need
   to find and use the raw display manager MIT-MAGIC-COOKIE file.
   Some examples for various display managers:

     gdm:     -auth /var/gdm/:0.Xauth
              -auth /var/lib/gdm/:0.Xauth
     kdm:     -auth /var/lib/kdm/A:0-crWk72
              -auth /var/run/xauth/A:0-crWk72
     xdm:     -auth /var/lib/xdm/authdir/authfiles/A:0-XQvaJk
     dtlogin: -auth /var/dt/A:0-UgaaXa

   Sometimes the command "ps wwwwaux | grep auth" can reveal the file location.

   Starting with x11vnc 0.9.9 you can have it try to guess by using:

              -auth guess

   (see also the x11vnc -findauth option.)

   Only root will have read permission for the file, and so x11vnc must be run
   as root (or copy it).  The random characters in the filenames will of course
   change and the directory the cookie file resides in is system dependent.
```
这似乎是因为桌面没有启动的原因，首先查看管理的文件的位置，`ps -ef | grep auth`
```
root     30195  1.0  1.9 521724 78216 tty1     Ssl+ 14:42   0:00 /usr/lib/xorg/Xorg -background none :0 -seat seat0 -auth /var/run/lightdm/root/:0 -nolisten tcp vt1 -novtswitch
root     30270  0.0  0.5 572428 22160 ?        Sl   14:42   0:00 /usr/lib/deepin-daemon/dde-authority
```
可以看到管理文件的位置在`/var/run/lightdm/root/:0`，启动是加入-auth参数并指定文件位置即可
```
sudo x11vnc -rfbport 5900 -rfbauth ~/.vnc/passwd -display :0 -forever -bg -repeat -nowf -auth /var/run/lightdm/root/:0 -o ~/.vnc/x11vnc.log
```
如果查询不到或许是桌面环境没有启动，如在deepin20可尝试`sudo service lightdm start`启动桌面环境。

## TigerVNC（<=1.10.0)的配置与使用（Centos8、Ubuntu20、18测试）

下文中使用的vncserver都是tigervncserver（旧版），不同的VNC使用都差不多，但是在xstart文件的配置可能有所不同，而且不同的桌面环境配置也不相同，下面使用的桌面环境都是Gnome。
###  安装tigervnc
```bash
# CentOS
sudo dnf install tigervnc-server
# ubuntu 
sudo apt install tigervnc-standalone-server
```
###  xstarup配置
下面两个配置，第一个只保留关键部分。
配置1，在CentOs及两个Ubuntu20上测试，其中一个Ubuntu灰屏，Ubuntu18按如下配置可正常显示。
```bash
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
gnome-session &
 
[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey
vncconfig -iconic &
```
 配置2，在CentOS测试，Ubuntu未测试
```bash
#!/bin/sh
 
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
OS=`uname -s`
if [ $OS = 'Linux' ]; then
  case "$WINDOWMANAGER" in
    *gnome*)
      if [ -e /etc/SuSE-release ]; then
        PATH=$PATH:/opt/gnome/bin
        export PATH
      fi
      ;;
  esac
fi
if [ -x /etc/X11/xinit/xinitrc ]; then
  exec /etc/X11/xinit/xinitrc
fi
if [ -f /etc/X11/xinit/xinitrc ]; then
  exec sh /etc/X11/xinit/xinitrc
fi
 
[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey
vncconfig -iconic &
xterm -geometry 8024+10+10 -ls -title "$VNCDESKTOP Desktop" &
twm &
# gnome-session &
gnome-session gnome
```
可能**需要重启**后才能正常使用。
### 启动vncsever
vncserver中常用的命令就是`vncserver`

```bash
# 开启一个端口
vncserver :20 # 如 :20 指定端口号为20，
# 停止一个端口
vncserver -kill :20
# 其他可选参数
vncserver :22 -localhost no # -localhost设置是否为本地端口
vncserver :22 -xstartup ./xstartup #指定xstartup文件
```
tigervnc默认`localhost=yes`即只能能通过本地连接，可在/etc/vnc.conf文件添加`$localhost = "no";`改变默认设置。

#### 访问远程桌面
使用VNC客户端，输入地址+端口就可以访问。如在realvnc中`192.168.194.236:22`
Tigervncserver默认使用本地端口，使用其他设备不能直接访问，可以在启动时加`-localhost no`参数指定端口可以让所有设备访问。
```bash
# 不使用 -localhost参数
vncserver :22
# 查看端口开放情况
netstat -ano | grep 5922
tcp        0      0 127.0.0.1:5922          0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp6       0      0 ::1:5922                :::*                    LISTEN      off (0.00/0/0)

# 使用 -localhost参数
vncserver :22 -localhost no
# 查看端口开放情况
netstat -ano | grep 5922
tcp        0      0 0.0.0.0:5922            0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp6       0      0 :::5922                 :::*                    LISTEN      off (0.00/0/0)
```
此外还可以使用ssh端口转发，或者使用iptables或firewall-cmd开发指定端口。如：

```bash
# ssh端口转发，访问使用127.0.0.1:5922
ssh -L 5922:127.0.0.1:5922 -N li@192.168.194.236
# firewall-cmd 开放端口
firewall-cmd --permanent --zoon=public --add-port=5901/tcp
# 或者端口范围
firewall-cmd --permanent --zoon=public --add-port=5900-5999/tcp
# 生效规则
firewall-cmd --reload
```
### 开机自启
旧版Tigervnc或其他vnc服务端可参考下面，本人试了几次没有完全成功。新版TigerVNC已使用systemed方式启动，可以很方便的设置开机自启。
[TigerVNC (简体中文) - ArchWiki](https://wiki.archlinux.org/index.php/TigerVNC_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#%E5%9C%A8%E5%BC%80%E5%85%B3%E6%9C%BA%E6%97%B6%E5%90%AF%E5%8A%A8%E5%85%B3%E9%97%AD_VNC_%E6%9C%8D%E5%8A%A1)

[systemd service file for running a vncserver (e.g. tightvncserver)](https://gist.github.com/spinxz/1692ff042a7cfd17583b)

### 问题及解决方案

同样的配置文件，一个用户可以正常连接，而另一个用户连接时灰屏，查看log文件发现有下面错误：
```
dbus[4643]: Unable to set up transient service directory: XDG_RUNTIME_DIR "/run/user/1000" is owned by uid 1000, not our uid 1002
```
经过排查，发现是因为在uid为1000的用户远程桌面，切换到uid为1002的用户开启vnc，此时系统变量`XDG_RUNTIME_DIR`为`/run/user/1000`，开启vnc是该变量仍然为原来用户所属路径。使用ssh登陆，重新开启vnc即可解决（临时把`XDG_RUNTIME_DIR`设置为`/run/user/1002`或也可以）。

#### 远程桌面显示问题

这个VNC是真滴玄学，都是Ubuntu20，都是tigervncserver，同样的xstartup文件，可是一个就可以正常，一个就是灰屏。灰屏的那个不使用xstartup能连接显示，但是锁屏后就不能输入密码解锁了。
同样的配置文件，在将虚拟机（RHEL 5）与主机（RHEL 6 + Vmware workstation）的共享目录作为用户目录时，使用VNC遇到灰屏问题，猜想或许时用户目录权限的问题，而且使用该用户在本机登陆桌面也不能成功登陆，会提示用户目录权限相关问题。

在redhat（realVNC、tigerVNC）上可用的xstartup文件，

```shell
#!/bin/sh
[ -r /etc/sysconfig/i18n ] && . /etc/sysconfig/i18n
export LANG
export SYSFONT
vncconfig -iconic &
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
OS=`uname -s`
if [ $OS = 'Linux' ]; then
  case "$WINDOWMANAGER" in
    *gnome*)
      if [ -e /etc/SuSE-release ]; then
        PATH=$PATH:/opt/gnome/bin
        export PATH
      fi
      ;;
  esac
fi
if [ -x /etc/X11/xinit/xinitrc ]; then
  exec /etc/X11/xinit/xinitrc
fi
if [ -f /etc/X11/xinit/xinitrc ]; then
  exec sh /etc/X11/xinit/xinitrc
fi
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey
xterm -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
twm &
```

同样的配置文件，一个用户可以正常连接，而另一个用户连接时灰屏，系统Ubuntu18.04，服务端tigervnc，xstartup配置文件：
```shell
#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS

[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey
vncconfig -iconic &
gnome-session &
```

#### authentication is required to create a color profile
有时遇到类似提示，可以取消或输入密码后提示界面是消失；有效时候提示界面可能回卡住，不能操作一直在顶层显示，可以考虑重启vnc服务，如每次出现可尝试采用下面方法处理。
1. 新建` /etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla`文件
```
[Allow Colord all Users]
Identity=unix-user:*
Action=org.freedesktop.color-manager.create-device;org.freedesktop.color-manager.create-profile;org.freedesktop.color-manager.delete-device;org.freedesktop.color-manager.delete-profile;org.freedesktop.color-manager.modify-device;org.freedesktop.color-manager.modify-profile
ResultAny=no
ResultInactive=no
ResultActive=yes
```

2. 修改`/usr/share/polkit-1/actions/org.freedesktop.color.policy`文件，将`allow_inactive`值改为`yes`.
```html
(....)  
<defaults> 
    <allow_any>auth_admin</allow_any> 
    <allow_inactive>yes</allow_inactive> 
    <allow_active>yes</allow_active> 
</defaults>
(...)
```

---

**参考**

1. [TigerVNC-ArcWiki](https://wiki.archlinux.org/index.php/TigerVNC#Installation)
2. [xRDP – The Infamous “Authentication Required to Create Managed Color Device” Explained – Griffon's IT Library](https://c-nergy.be/blog/?p=12073)
3. [xRDP – How to Fix the Infamous system crash popups in Ubuntu 18.04 (and previous versions) – Griffon's IT Library](http://c-nergy.be/blog/?p=12043)

---


**附录**CentOS中，TigerVNC升级后的使用说明文件。


# What has changed
The previous Tigervnc versions had a wrapper script called `vncserver` which 
could be run as a user manually to start *Xvnc* process. The usage was quite 
simple as you just run

```
$ vncserver :x [vncserver options] [Xvnc options]
```
and that was it. While this was working just fine, there were issues when users
wanted to start a Tigervnc server using *systemd*. For these reasons things were 
completely changed and there is now a new way how this all is supposed to work.

 # How to start Tigervnc server

## Add a user mapping
With this you can map a user to a particular port. The mapping should be done in 
`/etc/tigervnc/vncserver.users` configuration file. It should be pretty 
straightforward once you open the file as there are some examples, but basically
the mapping is in form

```
:x=user
```
For example you can have
```
:1=test
:2=vncuser
```

## Configure Xvnc options
To configure Xvnc parameters, you need to go to the same directory where you did
the user mapping and open `vncserver-config-defaults` configuration file. This 
file is for the default Xvnc configuration and will be applied to every user 
unless any of the following applies:

* The user has its own configuration in `$HOME/.vnc/config`
* The same option with different value is configured in 
  `vncserver-config-mandatory` configuration file, which replaces the default 
  configuration and has even a higher priority than the per-user configuration.
  This option is for system administrators when they want to force particular 
  *Xvnc* options.

Format of the configuration file is also quite simple as the configuration is
in form of

```
option=value
option
```
for example
```
session=gnome
securitytypes=vncauth,tlsvnc
desktop=sandbox
geometry=2000x1200
localhost
alwaysshared
```
### Note:
There is one important option you need to set and that option is the session you
want to start. E.g when you want to start GNOME desktop, then you have to use

```
session=gnome
```
which should match the name of a session desktop file from `/usr/share/xsessions`
directory.

## Set VNC password
You need to set a password for each user in order to be able to start the 
Tigervnc server. In order to create a password, you just run

```
$ vncpasswd
```
as the user you will be starting the server for. 
### Note:
If you were using Tigervnc before for your user and you already created a 
password, then you will have to make sure the `$HOME/.vnc` folder created by 
`vncpasswd` will have the correct *SELinux* context. You either can delete this 
folder and recreate it again by creating the password one more time, or 
alternatively you can run

```
$ restorecon -RFv /home/<USER>/.vnc
```

## Start the Tigervnc server
Finally you can start the server using systemd service. To do so just run
```
$ systemctl start vncserver@:x
```
as root or
```
$ sudo systemctl start vncserver@:x
```
as a regular user in case it has permissions to run `sudo`. Don't forget to 
replace the `:x` by the actual number you configured in the user mapping file. 
Following our example by running

```
$ systemctl start vncserver@:1
```
you will start a Tigervnc server for user `test` with a GNOME session.

### Note:
If you were previously using Tigervnc and you were used to start it using 
*systemd* then you will need to remove previous *systemd* configuration files,
those you most likely copied to `/etc/systemd/system/vncserver@.service`, 
otherwise this service file will be preferred over the new one installed with
latest Tigervnc.

# Limitations
You will not be able to start a Tigervnc server for a user who is already
logged into a graphical session. Avoid running the server as the `root` user as
it's not a safe thing to do. While running the server as the `root` should work 
in general, it's not recommended to do so and there might be some things which
are not working properly.

