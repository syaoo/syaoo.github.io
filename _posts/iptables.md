iptables详细教程：基础、架构、清空规则、追加规则、应用实例 - Lesca 技术宅: https://lesca.me/archives/iptables-tutorial-structures-configuratios-examples.html

iptables 添加，删除，查看，修改«海底苍鹰(tank)博客: http://blog.51yip.com/linux/1404.html

Linux系统启用端口转发（NAT）功能
```
# 非永久修改
echo 1 > /proc/sys/net/ipv4/ip_forward  
# 永久修改
vi /etc/sysctl.conf
net.ipv4.ip_forward=1
sysctl -p
```

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.0.2:80
sudo iptables -t nat -A POSTROUTING -p tcp -d 192.168.0.2 --dport 80 -j SNAT --to-source 127.0.0.1

sudo iptables -t nat -A PREROUTING -p tcp --dport 222 -j DNAT --to-destination 192.168.0.2:22
sudo iptables -t nat -A POSTROUTING -p tcp -d 192.168.0.2 --dport 22 -j SNAT --to-source 192.168.0.1

sudo iptables -t nat -A PREROUTING -p tcp --dport 5922 -j DNAT --to-destination 192.168.0.2:5922
sudo iptables -t nat -A POSTROUTING -p tcp -d 192.168.0.2 --dport 5922 -j SNAT --to-source 192.168.0.1