---
title: Linux远程桌面
tag: ['vnc','xrdp']
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
## vnc
个人感觉VNC的有点玄学，运气好的时候安装后启动就可以直接连接成功，否则就是出现各种黑屏、灰屏、无法连接等问题，而且同样的系统环境，同样的配置也可能一个可以用而另一个就不行。

### tigervncserver（Centos8、Ubuntu20测试）

下面使用的桌面环境都是Gnome。不同的桌面环境xstart文件的配置也不相同，
1. **安装tigervnc**
   
    ```bash
    # CentOS
    sudo dnf install tigervnc-server
    # ubuntu 
    sudo apt install tigervnc-standalone-server
    ```
2. xstarup配置
下面两个配置，第一个只保留关键部分。
配置1，在CentOs及两个Ubuntu上测试，其中一个Ubuntu灰屏
    ```
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
    ```
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
3. **vncsever使用**
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

4. **访问远程桌面**
    使用VNC客户端，输入地址+端口就可以访问。如在realvnc中`192.168.194.236:22`
    由于tigervncserver默认使用本地端口，使用其他设备不能直接访问，可以在启动时加`-localhost no`参数指定端口可以让所有设备访问。
    
    ```bash
    ## 不使用 -localhost参数
    vncserver :22
    # 查看端口开放情况
     netstat -ano | grep 5922
    tcp        0      0 127.0.0.1:5922          0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp6       0      0 ::1:5922                :::*                    LISTEN      off (0.00/0/0)
    
    ## 使用 -localhost参数
    vncserver :22 -localhost no
    # 查看端口开放情况
    netstat -ano | grep 5922
    tcp        0      0 0.0.0.0:5922            0.0.0.0:*               LISTEN      off (0.00/0/0)
    tcp6       0      0 :::5922                 :::*                    LISTEN      off (0.00/0/0)
    ```
此外还可以使用ssh端口转发，或者使用iptables或firewall-cmd开发指定端口。
如：

    ```bash
    ### ssh端口转发，访问使用127.0.0.1:5922
    ssh -L 5922:127.0.0.1:5922 -N li@192.168.194.236
    ### firewall-cmd 开放端口
    firewall-cmd --permanent --zoon=public --add-port=5901/tcp
    # 或者端口范围
    firewall-cmd --permanent --zoon=public --add-port=5900-5999/tcp
    # 生效规则
    firewall-cmd --reload
    ```

## 后记
这个VNC是真滴玄学，都是Ubuntu20，都是tigervncserver，同样的xstartup文件，可是一个就可以正常，一个就是灰屏。灰屏的那个不使用xstartup能连接，但是锁屏后就不能输入密码解锁了。

在redhat（realVNC、tigerVNC）上可用的xstartup文件，

```bash
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


###  x11vnc

之前使用的都是tigervnc之类的作为服务端但是总是不能很顺利的安装使用，同样的配置在不同的设备可能会有不同的效果。在Deepin20上测试。

1. 安装x11vnc：`sudo apt install x11vnc`
2. 密码设置: `x11vnc -storepasswd`
3. 启动服务器

```
  x11vnc -rfbport 5900 -rfbauth ~/.vnc/passwd -display :0 -forever -bg -repeat -nowf -o ~/.vnc/x11vnc.log
```

#### 启动失败解决方法
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
这似乎是因为桌面没有登陆的原因，首先查看管理的文件的位置，`ps -ef | grep auth`
```
root     30195  1.0  1.9 521724 78216 tty1     Ssl+ 14:42   0:00 /usr/lib/xorg/Xorg -background none :0 -seat seat0 -auth /var/run/lightdm/root/:0 -nolisten tcp vt1 -novtswitch
root     30270  0.0  0.5 572428 22160 ?        Sl   14:42   0:00 /usr/lib/deepin-daemon/dde-authority
```
可以看到管理文件的位置在`/var/run/lightdm/root/:0`，启动是加入-auth参数并指定文件位置即可
```
sudo x11vnc -rfbport 5900 -rfbauth ~/.vnc/passwd -display :0 -forever -bg -repeat -nowf -auth /var/run/lightdm/root/:0 -o ~/.vnc/x11vnc.log
```
如果查询不到或许是桌面环境没有启动，如在deepin20可尝试`sudo service lightdm start`启动桌面环境。


---

**参考**
1. [Azure: Installing GNOME desktop and xRDP to access an Ubuntu 17.10 Server - TechKB.onl]( https://www.techkb.onl/azure-installing-gnome-desktop-and-xrdp-to-access-an-ubuntu-1710-server/)
