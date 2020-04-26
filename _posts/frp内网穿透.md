最早了解内网穿透，是为了解决广域网联机玩游戏的问题，当时有使用向日葵、蛤蟆吃之类的工具，单体验都不是很好，最近再次研究内网穿透问题，除了游戏问题，还为了在在家能够访问内网工作，虽然有VPN可以访问内网，但是VPN软件在linux上不能正常使用。

这次研究了frp、ngrok、Zerotier、KSA几款软件。frp和ngork比较相似，都是针对端口进行穿透，二者都可以使用定义的转发服务器；不过frp支持点对点的穿透模式，能够实现内网服务器与客户端直连，不过在Symmetric NAT网络环境下不适用，ngrok有免费官方服务器可供使用，但是有时间限制，且每次运行都是随机地址。 Zerotier与KSA都是通过组建虚拟局域网的方式，使虚拟局域网内的设备可以互相访问。应用场景方面四款工具在内网访问使用NAS、游戏联机、访问内网应用中都适用，由于frp、ngrok可以不用客户端配合用于建站也是可以的。

## [FRP](https://github.com/fatedier/frp)

> > frp 是一个可用于内网穿透的高性能的反向代理应用，支持 tcp, udp 协议，为 http 和 https 应用协议提供了额外的能力，且尝试性支持了点对点穿透。可以windows、linux及macOS运行。
frp主要文件有四个：服务端程序frps、服务端配置文件frps.ini、客户端程序frpc、客户端配置文件frpc.ini；内网服务器使用frpc程序及其配置文件，具有静态公网IP的代理服务器使用frps程序及其配置文件。另外如果要使用**安全地暴露内网(stcp)**及**点对点内网穿透
(xtcp)**功能，还需要在访问内网服务器的设备上运行frpc程序。
点对点穿透可以实现内网服务器与外网客户端直接连接，仅有少量数据流量经过服务器。该功能处于开发的初级阶段，在Symmetric NAT网络环境下不能使用。



ngrok

Zerotier & KSA
Zerotier与KSA(看雪安全接入)都是组建虚拟局域网方式来连接内网服务器与外网客户端，优先使用点对点的连接方式，如果不能建立P2P连接则通过服务器转发。相比较而言，Zerotier功能更强大一些，能够管理局域网的设备、支持IPv6、可以自建被称为“Moon”的转发服务器。平台支持方面Zerotier能够在Win、Linux、Macos、iOS 、Android等平台运行，KSA目前支持Win、Mac以及linux。

参考：  

frp/README_zh.md at master · fatedier/frp: https://github.com/fatedier/frp/blob/master/README_zh.md#%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6





KSA Linux版发布！支持x86/x64、arm(64)和mips(el)，树莓派和路由器都可以运行了！-看雪安全接入-看雪安全论坛: https://bbs.pediy.com/thread-252417.htm

看雪学院: https://ksa.kanxue.com/index-down.htm

Manual – ZeroTier: https://www.zerotier.com/manual/
ngrok – documentation: https://ngrok.com/docs
zerotier内网穿透大局域网组建 | 月小升网络笔记: https://java-er.com/blog/zerotier-neiwang/
开始使用软件定义的网络并使用ZeroTier One创建VPN: https://www.howtoing.com/getting-started-software-defined-networking-creating-vpn-zerotier-one
Getting Started with ZeroTier - ZeroTier Knowledgebase - Confluence: https://zerotier.atlassian.net/wiki/spaces/SD/pages/8454145/Getting+Started+with+ZeroTier

扩展阅读：  
[NAT类型科普及一些简单提升NAT类型的方法 | 工作点滴]( https://www.zjzj.xyz/archives/927/)
[NAT类型概述以及提升NAT类型的方法 - 简书]( https://www.jianshu.com/p/478a4acc9d74)