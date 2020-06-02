## 服务端

### 安装[^1]

1. 在Ubuntu系统上使用apt安装（Debian应该也可以）
   
    ```bash
    sudo apt update
    sudo apt install shadowsocks-libev
    # 服务端命令ss-server
    # 客户端命令ss-local
    # 另外还有一个shadowsocks,与下面pip安装的一样，已经停止更新版本不建议使用
    ```
2. 使用Python:shadowsocks-python  
   
    ```bash
    # 需要Python2.6或2.7, Python3也可以但是要修改一个文件
    sudo pip install shadowsocks
    sudo ln -s /usr/local/python/bin/sslocal /usr/bin/sslocal  #不是必须
    # 服务端命令ssserver
    # 客户端命令sslocal
    ```


## 服务端配置
shadowsocks-libev的配置默认文件在`/etc/shadowsocks-libev/config.json`
也可以新建一个配置文件使用：
 ```bash
 {
 "server":"0.0.0.0",
 "server_port":your_server_port, # 服务器使用端口
 "local_address":"127.0.0.1",
 "local_port":1080,
 "password":"your_server_passwd",  # 连接密码
 "timeout":300,
 "method":"aes-256-gcm" # 此外其他多种加密方式可选，如：
 # aes-128-gcm, aes-192-gcm, chacha20-ietf-poly1305, xchacha20-ietf-poly1305
 }
 ```
### 启动
1. 以服务形式启动，使用默认配置文件
 ```bash
 # Start
sudo systemctl start shadowsocks-libev.service
# Stop
sudo systemctl stop shadowsocks-libev.service
# Restart
sudo systemctl restart shadowsocks-libev.service
 ```
2. 使用`ss-server`启动
 ````bash
 # `ss-server -h`查看帮助
 sudo ss-server -c ./shadowsocks.conf -d start	#可使用指定配置文件
 ````
## 开启TCP BBR加速

如果linux内核版本高于4.9，那就可以直接按下面步骤开启BBR，否则需要升级内核(`uname -a`查看内核信息)。
1.修改系统变量(需要root权限)：

 ```
 echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
 echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
 ```
2.保存设置`sysctl -p`

3.查看是否开启成功
 ```bash
 # 如果开启成功应有以下相同或类似输出
 sysctl net.ipv4.tcp_available_congestion_control
 # net.ipv4.tcp_available_congestion_control = reno cubic bbr
 sudo sysctl -n net.ipv4.tcp_congestion_control
 # bbr
 lsmod | grep bbr
 # tcp_bbr                20480  3
 ```

## 客户端

Windows与Android系统客户端使用比较方便，直接从github上下载安装相应的客户端即可。iOS上在国内Appstore上目前应该没有可以下载的客户端，在美区似乎有shadowrocket可以下载使用。linux上图形化、命令行客户端，不过使用起来没有Win、Android上方便。
### windows
shadowsocks/shadowsocks-windows: https://github.com/shadowsocks/shadowsocks-windows/releases
### Android	
shadowsocks/shadowsocks-android: https://github.com/shadowsocks/shadowsocks-android/releases
### Linux
图形化客户端：[outline-client](https://github.com/Jigsaw-Code/outline-client)（全平台通用，但是只能全局使用）、[electron-ssr](https://github.com/qingshuisiyuan/electron-ssr-backup)（已停止维护）、[shadowsocks-qt5](https://github.com/shadowsocks/shadowsocks-qt5)（已停止维护）
命令行客户端：ss-local(shadowsocks-libev内置)、sslocal(shadowsocks内置)
上面几种客户端图形界面一般使用都比较简单，命令行还需有一些额外的设置。
#### ss-local配置

ss-local的配置文件(/etc/shadowsocks-libev/config.json)与ss-server配置差不多，把server改为服务器地址即可。
   ```bash
 {
 "server":"server_ip",
 "server_port":your_server_port, # 服务器使用端口
 "local_address":"127.0.0.1",
 "local_port":1080,
 "password":"your_server_passwd",  # 连接密码
 "timeout":300,
 "method":"aes-256-gcm" # 此外其他多种加密方式可选，如：
 # aes-128-gcm, aes-192-gcm, chacha20-ietf-poly1305, xchacha20-ietf-poly1305
 }
   ````
Shadowsocks-libev安装后默认会以服务的形式自动运行ss-server，可以通过将`/lib/systemd/system/shadowsocks-libev.service`文件中的`ExecStart=/usr/bin/ss-server -c $CONFFILE $DAEMON_ARGS`改为`ExecStart=/usr/bin/ss-local -c $CONFFILE $DAEMON_ARGS`来实现自动运行ss-local。
   ```bash
   #重新加载shadowsocks-libev.service
   sudo systemctl daemon-reload
   #启动shadowsocks-libev.service，此时启动为客户端ss-local
   sudo systemctl start shadowsocks-libev.service
   ```
   
#### 系统代理设置
在系统设置-网络-网络代理可以进行代理设置，其中有自动与手动选项，前者可以借助pac文件实现仅对外网进行代理（pac模式），而后者则会对所以网站使用代理（全局模式）。（在测试中发现，在不能实现Terminal外网访问。）
1、全局模式
这里的socks host是配置文件中的`local_address`本地地址,端口为配置文件中`local_port`,一般为1080。
![tt6KvF.png](https://s1.ax1x.com/2020/06/02/tt6KvF.png)
*通常启动ss-local，设置好代理后就可以正常使用了，但是我在Ubuntu 20 虚拟机中测试始终无法正常上网，然而在firefox浏览器中做同样的代理设置却可以正常使用，不知是何原因。*

2、pac模式
![tt6n3T.png](https://s1.ax1x.com/2020/06/02/tt6n3T.png)
如图，在url中填入pac文件路径，即可启用pac模式。pac文件可以使用genpac生成。
   ```bash
    # 安装
    sudo pip3 install genpac
    # 生成pac文件
    genpac --pac-proxy "SOCKS5 127.0.0.1:1080" --output="autoproxy.pac" --gfwlist-url="https://pagure.io/gfwlist/raw/master/f/gfwlist.txt" --user-rule-from="user-rules.txt"
   ```
   genpac参数中，--output指定pac文件，如这里是当前目录下的autoproxy.pac，然后在代理设置中填写的url地址为“file:///home/user/.shadowsocks/pac/autoproxy.pac“，--user-rule-from指定的自定义规则文件，该文件中可以添加自己的规则，规则修改后需要重新生成pac文件才能生效。  
   关于genpac的更多内容及gfwlist可以参加这两个repo：https://github.com/JinnLynn/genpac、https://github.com/gfwlist/gfwlist；自定义规则可以参考这里：https://adblockplus.org/en/filter-cheatsheet

## Oracle Cloud

https://wzfou.com/oracle-ip-root/

---

参考:  
[一键脚本搭建ss 一键脚本搭建ssr 一键开启bbr ss/ssr一键 - flyzy小站](https://www.flyzy2005.com/fan-qiang/shadowsocks/install-shadowsocks-in-one-command/#BBR)  
[Shadowsocks-libev 服务端的部署](https://cokebar.info/archives/767)  
[shadowsocks/shadowsocks-libev: libev port of shadowsocks] (https://github.com/shadowsocks/shadowsocks-libev)  
[Ubuntu配置Shadownsocks以及配置pac规则 | 雾非雾的情思](https://www.mspring.org/2018/11/17/Ubuntu%E9%85%8D%E7%BD%AEShadownsocks%E4%BB%A5%E5%8F%8A%E9%85%8D%E7%BD%AEpac%E8%A7%84%E5%88%99/)


[^1]: [Shadowsocks - Servers](https://shadowsocks.org/en/download/servers.html)