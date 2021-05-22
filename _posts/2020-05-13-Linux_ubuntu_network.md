---
title: Ubuntu虚拟机无法连接网络
tag: ["ubuntu"]
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover1.jpg
---
Ubuntu虚拟机从Vmware迁移到Vbox，出现无法连接网络的问题。在排除虚拟机设置问题后，确认问题原因应在Ubuntu系统中，最终通过删除NetworkManager.state文件，并重启network-manager服务解决问题。
<!--more-->

## 起因及问题
为避免使用无合法授权软件，考虑将虚拟机从正在使用的Vmware迁移到Vbox，成功从Vmware导出ovf文件，并导入Vbox后，win7系统一切正常，然而而Ubuntu 20.04无法连接网络。表现为状态栏没有网络连接图标，设置-网络连接中也仅有VPN设置项。
## 问题解决
修改虚拟机的网络连接方式为NAT与桥接网卡均无效，测试重新安装虚拟机则可以正常连接，排除虚拟机设置问题，或为Ubuntu系统问题。从文章1发现类似问题解决办法，参考其方案：
```bash
# 1. 停止network-manager服务
sudo service network-manager stop
# 2. 删除/var/lib/NetworkManager/NetworkManager.state文件
sudo rm /var/lib/NetworkManager/NetworkManager.state
# 3. 启用network-manager服务
sudo service network-manager start
```
进行上述操作后，系统网络很快恢复。
NetworkManager.state文件内容如下：

```
[main]
NetworkingEnabled=true
WirelessEnabled=true
WWANEnabled=true
```
对原始与比新生成的NetworkManager.state，发现原始文件中`NetworkingEnabled`值为`false`。停止network-manager服务，将NetworkingEnabled改为false后在启动，复现无法连接网络的问题。因此虚拟机出现该故障的原因应该是该配置文件的问题，然而在Vmware中的该虚拟机的NetworkManager.state文件是正常的，在[NetworkManager Wiki](https://wiki.archlinux.org/index.php/NetworkManager_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#%E7%BD%91%E7%BB%9C%E7%AE%A1%E7%90%86%E5%8A%9F%E8%83%BD%E5%A4%B1%E6%95%88)中也提到类似问题及原因，或许是在虚拟机迁移过程中意外出现“NetworkManager关闭了，但对应的pid文件却没有移除”。

**参考**

1. [Ubuntu 网络连接图标消失 解决方法_运维_Step Up-CSDN博客](https://blog.csdn.net/flying881114/article/details/6847579)