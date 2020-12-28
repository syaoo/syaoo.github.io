---
title: 使用Systemd管理服务（开机自启）
tag: ['linux', 'systemctl']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---

自定义系统服务，并设置开机自启。两步实现：配置systemd文件、设置自启。

<!--more-->

Systemd 是 Linux 系统工具，用来启动守护进程，已成为大多数发行版的标准配置。Systemd有一系列命令组成，如`systemctl`、`systemd-analyze`、`hostnamectl`、`localectl`等。

## 命令使用

服务管理通常使用`systemctl`命令即可，这里只是列出了各命令的部分使用，更多使用方法可以查看帮助文档。

### systemctl

使用systemctl命令管理系统服务Unit的

```shell
systemctl enable nginx # 开机启动
systemctl is-enabled nginx # 查看服务是否开机启动
systemctl disable nginx  # 关闭开机启动
systemctl start nginx  # 启动服务
systemctl stop nginx # 停止服务
systemctl restart nginx # 重启服务
systemctl status nginx # 查看服务状态(详细信息)
systemctl is-active nginx # 查看服务是否活动
systemctl kill nginx # 结束服务进程(服务无法停止时)
systemctl daemon-reload # 添加或修改配置文件后，使改动生效
systemctl --failed # 查看启动失败的服务
```

###  其他命令

1. `loginctl`
   ```shell
   # 列出当前session
   loginctl list-sessions
   # 列出当前登录用户
   loginctl list-users
   # 列出显示指定用户的信息
   loginctl show-user ruanyf
   ```

2. `timedatectl`
   ```shell
   # 查看当前时区设置
   timedatectl
   # 显示所有可用的时区
   timedatectl list-timezones
   # 设置当前时区
   timedatectl set-timezone America/New_York
   timedatectl set-time YYYY-MM-DD
   timedatectl set-time HH:MM:SS
   ```
3. `hostnamectl`
   ```shell
   # 显示当前主机的信息
   hostnamectl
   # 设置主机名。
   hostnamectl set-hostname rhel7
   ````
4. `systemd-analyze`
   ```shell
   # 查看启动耗时
   systemd-analyze 
   # 查看每个服务的启动耗时
   systemd-analyze blame
   # 显示瀑布状的启动过程流
   systemd-analyze critical-chain
   # 显示指定服务的启动流
   systemd-analyze critical-chain atd.service
   ```

## 服务配置文件

配置文件通常分用户`user`和系统`system`配置文件，分别放在相应的目录内，通常存储在在 `/usr/lib/systemd/`目录下，有时也在 `/etc/systemd/` 目录下即，`/user/lib/systemd/system/`、`/user/lib/systemd/user/`和`/etc/systemd/system/`、`/etc/systemd/user/`。

Systemd 默认从目录`/etc/systemd/system/`读取配置文件。但是，里面存放的大部分文件都是符号链接，指向目录`/usr/lib/systemd/system/`，真正的配置文件存放目录。

sshd服务的配置文件;

```yaml
[Unit]
Description=OpenSSH server daemon
Documentation=man:sshd(8) man:sshd_config(5)
After=network.target sshd-keygen.service
Wants=sshd-keygen.service

[Service]
Type=notify
EnvironmentFile=/etc/sysconfig/sshd
ExecStart=/usr/sbin/sshd -D $OPTIONS
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartSec=42s

[Install]
WantedBy=multi-user.target
```

服务的配置文件以`.service`作为扩展名，通常有三个区块`Unit`，`Service`，`Install`。

### 配置文件说明
详细的配置文件信息可参考[官方文档](https://www.freedesktop.org/software/systemd/man/systemd.unit.html)

1. `Unit`区块通常是配置文件的第一个区块，用来定义 Unit 的元数据，以及配置与其他 Unit 的关系。它的主要字段如下。
```
Description：当前服务的简单描述
Documentation：指定 man 文档位置

After：如果 network.target 或 sshd-keygen.service 需要启动，那么 sshd.service 应该在它们之后启动
Before：定义 sshd 应该在哪些服务之前启动
注意：After 和 Before 字段只涉及启动顺序，不涉及依赖关系。

Wants：表示 sshd.service 与 sshd-keygen.service 之间存在"弱依赖"关系，即如果"sshd-keygen.service"启动失败或停止运行，不影响 sshd.service 继续执行
Requires：表示"强依赖"关系，即如果该服务启动失败或异常退出，那么sshd.service 也必须退出
注意：Wants 字段与 Requires 字段只涉及依赖关系，与启动顺序无关，默认情况下是同时启动。
```
 2. `Service`通常是配置文件的最后一个区块，用来定义如何启动，以及是否开机启动。它的主要字段如下。
```
EnvironmentFile：许多软件都有自己的环境参数文件，该字段指定文件路径
注意：/etc/profile 或者 /etc/profile.d/ 这些文件中配置的环境变量仅对通过 pam 登录的用户生效，而 systemd 是不读这些配置的。
systemd 是所有进程的父进程或祖先进程，它的环境变量会被所有的子进程所继承，如果需要给 systemd 配置默认参数可以在 /etc/systemd/system.conf  和 /etc/systemd/user.conf 中设置。加载优先级 system.conf 最低，可能会被其他的覆盖。

Type：定义启动类型。可设置：simple，exec，forking，oneshot，dbus，notify，idle
simple(设置了 ExecStart= 但未设置 BusName= 时的默认值)：ExecStart 字段启动的进程为该服务的主进程
forking：ExecStart 字段的命令将以 fork() 方式启动，此时父进程将会退出，子进程将成为主进程

ExecStart：定义启动进程时执行的命令
上面的例子中，启动 sshd 执行的命令是 /usr/sbin/sshd -D $OPTIONS，其中的变量 $OPTIONS 就来自 EnvironmentFile 字段指定的环境参数文件。类似的，还有如下字段：
ExecReload：重启服务时执行的命令
ExecStop：停止服务时执行的命令
ExecStartPre：启动服务之前执行的命令
ExecStartPost：启动服务之后执行的命令
ExecStopPost：停止服务之后执行的命令

RemainAfterExit：设为yes，表示进程退出以后，服务仍然保持执行

KillMode：定义 Systemd 如何停止服务，可以设置的值如下：
control-group（默认值）：当前控制组里面的所有子进程，都会被杀掉
process：只杀主进程
mixed：主进程将收到 SIGTERM 信号，子进程收到 SIGKILL 信号
none：没有进程会被杀掉，只是执行服务的 stop 命令

Restart：定义了退出后，Systemd 的重启方式。可以设置的值如下：
no（默认值）：退出后不会重启
on-success：只有正常退出时（退出状态码为0），才会重启
on-failure：非正常退出时（退出状态码非0），包括被信号终止和超时，才会重启
on-abnormal：只有被信号终止和超时，才会重启
on-abort：只有在收到没有捕捉到的信号终止时，才会重启
on-watchdog：超时退出，才会重启
always：不管是什么退出原因，总是重启

RestartSec：表示 Systemd 重启服务之前，需要等待的秒数
```
3. `Install`通常是配置文件的最后一个区块，用来定义如何启动，以及是否开机启动。它的主要字段如下。
```
WantedBy：表示该服务所在的 Target(服务组) ，它的值是一个或多个 Target，当前 Unit 激活时（enable）符号链接会放入/etc/systemd/system目录下面以 Target 名 + .wants后缀构成的子目录中
RequiredBy：它的值是一个或多个 Target，当前 Unit 激活时，符号链接会放入/etc/systemd/system目录下面以 Target 名 + .required后缀构成的子目录中
Alias：当前 Unit 可用于启动的别名
Also：当前 Unit 激活（enable）时，会被同时激活的其他 Unit
```
## 自定义服务并配置开机自启

将gossa文件服务添加到系统服务，并设置自启。

### 编辑配置文件

```yaml
# /usr/lib/systemd/system/gossa.service
[Unit]
Description=文件服务器
After=network.target
Wants=nginx.service # 该nginx用于端口转发，所有要启动nginx，但不是必须
[Service]
# 使用环境变量
Environment=SHARE_DIR=/home/vgos/hdisk/share
ExecStart=/usr/local/etc/gossa/gossa-linux64 -h "0.0.0.0" $SHARE_DIR
# 不使用环境变量
#ExecStart=/usr/local/etc/gossa/gossa-linux64 -h "0.0.0.0" /home/vgos/hdisk/share
ExecReload=/bin/kill -HUP $MAINPID
[Install]
WantedBy=multi-user.target
```

### 应用配置文件及开机自启

```
# 添加或修改配置文件后，需要重新加载
systemctl daemon-reload

# 设置自启动，实质就是在 /etc/systemd/system/multi-user.target.wants/ 添加服务文件的链接
systemctl enable gossa
```

## 自动挂载网络服务器

[Mount a volume using systemd - DEV](https://dev.to/adarshkkumar/mount-a-volume-using-systemd-1h2f)
[使用systemd挂载文件系统 - jTree Home](https://jtree.cc/post/%E4%BD%BF%E7%94%A8systemd%E6%8C%82%E8%BD%BD%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F/)

**参考**

1. [Systemd 添加自定义服务(开机自启动) - 江湖小小白 - 博客园](https://www.cnblogs.com/jhxxb/p/10654554.html)
2. [systemctl 实现开机自启服务_qq_29663071的博客-CSDN博客](https://blog.csdn.net/qq_29663071/article/details/80814081)
3. [Systemd 入门教程：命令篇 - 阮一峰的网络日志](http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html)
