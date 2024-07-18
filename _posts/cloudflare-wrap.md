综合网上信息wrap与wrap+区别在于wrap+会对线路进行优化

Cloudflare Wrap(WARP)是Cloudflare提供的一项基于WireGuard的网络流量安全及加速服务，能够让你通过连接到Cloudflare的边缘节点实现隐私保护及链路优化。也可以借助该服务为仅有IPv4或IPv6单栈出口的服务器配置IPv4\IPv6双栈出口。

## Wrap官方客户端

官方客户端支持
[1.1.1.1 — The free app that makes your Internet faster.](https://1.1.1.1/)

## 使用WireGuard客户端

据[博文8](https://p3terx.com/archives/cloudflare-warp-script-issue-and-solution.html)所述，由于Cloudflare未来将采用私有协议，同时放弃WireGuard的兼容，该方案未来有可能不能使用。

2.1 提取CloudFlare wrap的WireGuard配置信息

前两个出自同一个作者似乎都是基于wgcf编写的脚本

[warpgo-profile-generator - Replit](https://replit.com/@misaka-blog/warpgo-profile-generator)
[wgcf-profile-generator - Replit](https://replit.com/@misaka-blog/wgcf-profile-generator)
[GitHub-ViRb3/wgcf: Cross-platform, unofficial CLI for Cloudflare Warp](https://github.com/ViRb3/wgcf)

2.2 优先节点IP
默认节点可能无法连接，新版官方客户端无法更改节点（下面文章说6.9和6.10版本可以修改）

win客户端安装路径下有warp-cli.exe工具，可以用于修改节点设置

```bat
@rem 将节点修改为162.159.192.1:2408
warp-cli.exe clear-custom-endpoint
warp-cli.exe set-custom-endpoint 162.159.192.1:2408
```

3. 使用wrap为vps增加ipv4/ipv6出口


## 开通Zero Trust并启用Wrap

下图是开通Zero Trust的操作流程，登陆CloudFlare账户，点击右侧Zero Trust菜单进入开通流程，按提示操作即可进入Zero Trust控制面板。需要注意的是在第4步中可能需要添加信用卡才可以进入下一步，即可进入控制面板（下图第6步）。其实到这里可以直接输入地址进入[Zero Trust](https://one.dash.cloudflare.com)，跳过填写信用卡，不过这里虽然可以不添加信用卡，但是要开通使用Wrap还是需要添加信用卡，这一步没有发现可以跳过的方法。

![开通Zero Trust]()

进入Zero Trust后，点击"Settings"，按下图操作启用"Wrap Client"。

![启用Wrap Client]()

进入Wrap Clien，点击界面中Manage，添加设备控制注册规则。规则设置内容如下图所示。其中Rule Action有四种选择，可以选择允许、禁用等规则。Selector项可以选择按邮箱地址(Emails)或邮箱服务器(Emails Ending in)匹配规则。设置完成一条规则后可以点击下面"+Add include"增加其他包含规则。符合规则的邮箱将被运行或禁止登陆Zero Trust。

设置好规则后，可以在客户端登陆到Zero Trust使用Wrap，客户端设置中找到账户，其中有登陆到Zero Trust选项，按提示输入团队名称（前面开通过程中输入的团队名称，可以在Zero Trust控制面板Settings-Custom Pages中找到），输入登陆邮箱，系统将向该邮箱发送验证码，填写正确验证码即可登陆。

1. [关于 Cloudflare Warp 的一些细节以及是否暴露访客真实 IP 的测试 | Sukka's Blog](https://blog.skk.moe/post/something-about-cf-warp/)
2. [在WireGuard客户端上使用CloudFlare WARP节点](https://blog.misaka.rest/2023/01/25/wireguard-warp/)
3. [优选WARP的EndPoint IP，提高本地WARP节点访问性并修改各客户端的EndPoint IP](https://blog.misaka.rest/2023/03/12/cf-warp-yxip/)
4. [Cloudflare WARP 教程：给 VPS 额外添加“原生” IPv4/IPv6 双栈网络出口 - P3TERX ZONE](https://p3terx.com/archives/use-cloudflare-warp-to-add-extra-ipv4-or-ipv6-network-support-to-vps-servers-for-free.html)
5. [https://www.wangwangit.com/WARP/](https://www.wangwangit.com/WARP/)
6. [申请CloudFlare Teams（Zero Trust）账户教程](https://blog.misaka.rest/2023/02/08/cf-teams/)
7. [MisakaNo の 小破站 / warp-script · GitLab](https://gitlab.com/Misaka-blog/warp-script/)
8. [Cloudflare WARP 脚本已知问题和解决方法 - P3TERX ZONE](https://p3terx.com/archives/cloudflare-warp-script-issue-and-solution.html)