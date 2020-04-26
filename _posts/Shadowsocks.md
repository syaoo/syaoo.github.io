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

### windows使用
shadowsocks/shadowsocks-windows: https://github.com/shadowsocks/shadowsocks-windows/releases
### Android	
shadowsocks/shadowsocks-android: https://github.com/shadowsocks/shadowsocks-android/releases
### Linux使用
图形化客户端：outline-client，electron-ssr
cli：ss-local(shadowsocks-libev包含的客户端命令)
#### 说明
如果不需要终端走HTTP上网，仅仅需要浏览器代理上网的话，推荐使用[SwitchyOmega](https://www.switchyomega.com/)浏览器插件来管理代理上网，这个插件很强大、很灵活，配置起来也很简单，这里就不多做累述了。
下面的步骤是配置全局使用HTTP代理。

## Privoxy篇 -- 将Socks5转换为HTTP代理
1. 使用`sudo apt install privoxy`安装

2. 编辑配置文件`/etc/privoxy/config`  
找到 `listen-address` 改为 `listen-address 127.0.0.1:端口号` 
找到 `forward-socks5` 确保有这行代码并且打开注释(没有自己加)` forward-socks5 / 127.0.0.1:1080 .`
在文件末尾加上`actionsfile gfwlist.action`（等会就知道这个文件是干嘛用的了）

3. 启动privoxy
    ```bash
    sudo service privoxy start
    sudo service privoxy status
    ```
    配置环境变量，让终端也能走代理，全局环境变量位置`/ect/profile`,用户环境变量位置` ~/.bash_profile`,`~/.bashrc`文件末尾处都添加上以下内容
    ```bash
    proxy="http://127.0.0.1:端口"
    export https_proxy=$proxy
    export http_proxy=$proxy
    export ftp_proxy=$proxy
    ```
### 使用PAC

安装 GFWList2Privoxy

 ```bash
 pip install --user gfwlist2privoxy
 ```
获取gfwlist文件，生成actionsfile
 ```bash
 cd /tmp
 wget https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt
 ~/.local/bin/gfwlist2privoxy -i gfwlist.txt -f gfwlist.action -p 127.0.0.1:1080 -t socks5
 sudo cp gfwlist.action /etc/privoxy/
 ```
重启Privoxy，测试代理是否走了pac模式

 ```bash
 curl www.google.com	#测试谷歌是否可以访问
 curl "http://pv.sohu.com/cityjson?ie=utf-8" #测试是否应用pac
 ```

## 开机自启
方法一、编辑rc.loacl。

方法二、init.d
1. 创建启动脚本,并修改脚本权限为755
    ```bash
    #!/bin/bash
    sslocal -c /etc/shadowsocks.json -d start
    ```
2. 将脚本放置在`/etc/init.d`中

4.将脚本添加到启动脚本。
    ```bash
    # 在这里`90`表明一个优先级，越高表示执行的越晚
    cd /etc/init.d/
    sudo update-rc.d shadowsocks.sh default 90
    ```
#### 配置代理
系统设置-网络-网络代理，设置socks5代理；自动为全局代理、手动可以设置PAC。
#### PAC模式
 ```
 # 安装
 sudo apt install genpac
 # 启动
 genpac --proxy="SOCKS5 127.0.0.1:1080" --gfwlist-proxy="SOCK5 127.0.0.1:1080" -o autoproxy.pac --gfwlist-url="https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
 ```

#### Oracle Cloud

https://wzfou.com/oracle-ip-root/

---

参考:  
[一键脚本搭建ss 一键脚本搭建ssr 一键开启bbr ss/ssr一键 - flyzy小站](https://www.flyzy2005.com/fan-qiang/shadowsocks/install-shadowsocks-in-one-command/#BBR)  
[Shadowsocks-libev 服务端的部署](https://cokebar.info/archives/767)  
[shadowsocks/shadowsocks-libev: libev port of shadowsocks] (https://github.com/shadowsocks/shadowsocks-libev)  

[^1]: [Shadowsocks - Servers](https://shadowsocks.org/en/download/servers.html)