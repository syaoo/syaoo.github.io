---
title: systemctl使用（开机自启）
tag: ['systemctl','开机自启']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---

abstract

<!--more-->

## 命令使用

```
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



**参考**
1. [Systemd 添加自定义服务(开机自启动) - 江湖小小白 - 博客园](https://www.cnblogs.com/jhxxb/p/10654554.html)
2. [systemctl 实现开机自启服务_qq_29663071的博客-CSDN博客](https://blog.csdn.net/qq_29663071/article/details/80814081)
