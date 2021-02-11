ubuntu19.4 网络配置：

```bash
cat /etc/netplan/50-cloud-init.yaml
# This file is generated from information provided by
# the datasource.  Changes to it will not persist across an instance.
# To disable cloud-init's network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    ethernets:
        enp3s0:
            addresses:
            - 202.127.29.131/24
            gateway4: 202.127.29.1
            nameservers:
                addresses:
                - 202.127.28.4
                - 159.226.8.7
                search:
                - baidu.com
    version: 2
```

linux网络打印机：

安装驱动（linux-UFRII-drv-v500-sc-16.tar.gz）

设置默认打印机：``# lpadmin -d [printer-name]``

查看默认打印机： ``# lpstat -d``

查看打印机列表：``#lpstat -s``



关闭图形界面，默认命令行 `sudo systemctl set-default multi-user.target`

开启图形界面，默认图新界面 `sudo systemctl set-default graphical.target`

临时开启 `sudo systemctl start lightdm`

`.vnc/xstartup`

```bash
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
startxfce4 &

[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey
vncconfig -iconic &

-------------------------------
Make sure VNC is installed in the system.
Edit $HOME/.vnc/xstartup.
Uncomment : unset SESSION_MANAGER
Uncomment : exec /etc/X11/xinit/xinitrc
Comment : xterm -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
Comment : twm &
Add "gnome-session &" under the "exec /etc/X11/xinit/xinitrc" line.
The Xstartup file should look like this (Red: added line, Blue: modified line) :
----------
#!/bin/sh

# Uncomment the following two lines for normal desktop:
unset SESSION_MANAGER
exec /etc/X11/xinit/xinitrc
gnome-session &

[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey
vncconfig -iconic &
#xterm -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
#twm &
----------
Run "vncserver :1" to start the vnc session with the GNOME desktop loaded in.
Connect to the machine and the VNC session will present the GNOME desktop. 
```



### 删除软件

```bash
# 删除软件及其配置文件
apt-get --purge remove <package>
# 删除没用的依赖包
apt-get autoremove <package>
# 此时dpkg的列表中有“rc”状态的软件包，可以执行如下命令做最后清理：
dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P
# 当然如果要删除暂存的软件安装包，也可以再使用clean命令。
apt-get clean <package>
```

### Deepin VNCSERVER

安装VNC

`sudo apt install tigervnc-standalone-server tigervnc-common`

```
#~.vnc/xstartup
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec /etc/X11/xinit/xinitrc
```

启动VNCSERVER

`vncsever :01 -localhost no `OR`vncsever -localhost :01 `



### dpkg使用

1、dpkg -i <package.deb>
安装一个 Debian 软件包，如你手动下载的文件。

2、dpkg -c <package.deb>
列出 <package.deb> 的内容。

3、dpkg -I <package.deb>
从 <package.deb> 中提取包裹信息。

4、dpkg -r <package>
移除一个已安装的包裹。

5、dpkg -P <package>
完全清除一个已安装的包裹。和 remove 不同的是，remove 只是删掉数据和可执行文件，purge 另外还删除所有的配制文件。

6、dpkg -L <package>
列出 <package> 安装的所有文件清单。同时请看 dpkg -c 来检查一个 .deb 文件的内容。

7、dpkg -s <package>
显示已安装包裹的信息。同时请看 apt-cache 显示 Debian 存档中的包裹信息，以及 dpkg -I 来显示从一个 .deb 文件中提取的包裹信息。

8、dpkg-reconfigure <package>
重新配制一个已经安装的包裹，如果它使用的是 debconf (debconf 为包裹安装提供了一个统一的配制界面)。

#### set PATH
```bash
# Add /usr/local/texlive/2019/texmf-dist/doc/man to MANPATH.
# Add /usr/local/texlive/2019/texmf-dist/doc/info to INFOPATH.
# Most importantly, add /usr/local/texlive/2019/bin/x86_64-linux
# to your PATH for current and future sessions.
```
These 2 are almost the same:
```bash
export PATH=/usr/share/lib/something:$PATH 
export PATH=$PATH:/usr/share/lib/something
```
The only difference is that the first one puts the directory to add in front and the second one puts it behind the current directories in $PATH. It only matters if there are commands inside /usr/share/lib/something that have the same name inside one of the directories in $PATH.

To add directories to $MANPATH or $INFOPATH as required from the link you posted you do that by changing the config files inside the link.

It says to open the global version of bash.bashrc with:
```bash
sudo vi /etc/bash.bashrc
```
and to add at the end:
```bash
PATH=/usr/local/texlive/2010/bin/x86_64-linux:$PATH; export PATH
MANPATH=/usr/local/texlive/2010/texmf/doc/man:$MANPATH; export MANPATH
INFOPATH=/usr/local/texlive/2010/texmf/doc/info:$INFOPATH; export INFOPATH
```
This sets $PATH, $MANPATH and $INFOPATH. And it also tells you to edit /etc/manpath.config with:
```bash
sudo vi /etc/manpath.config
```
and to add
```bash
MANPATH_MAP /usr/local/texlive/2010/bin/x86_64-linux /usr/local/texlive/2010/texmf/doc/man
```
underneath # set up PATH to MANPATH mapping.

If you are unsure about this make a backup 1st (never a bad thing) with:

sudo cp /etc/bash.bashrc /etc/bash.backup_$(date +"%Y_%m_%d").bashrc
sudo cp /etc/manpath.config /etc/manpath.backup_$(date +"%Y_%m_%d").config
