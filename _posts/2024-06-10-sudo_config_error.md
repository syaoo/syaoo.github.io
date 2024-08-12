---
title: sudo权限配置的错误的补救措施
tag: ['linux', 'sudo']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover1.jpg
---

记录一次sudo权限配置的错误操作及补救措施。

<!--more-->

<!-- # 一次sudo权限配置的错误操作及补救 -->

通常情况下修改sudo权限配置文件(/etc/sudoers或/etc/sudoers.d/) **需要使用visudo完成**，该工具打开文件进行编辑，并在退出时检查文件内容是否正确。

但在某次配置中我竟然直接`sudo cp /etc/sudoers.d/a /etc/sudoers.d/b`复制了一份，想着在原来的基础上修改，但是当执行`sudo vim /etc/sudoers.d/b`的时候却突然报错

```
>>> /etc/sudoers.d/b: Alias "COMMAND_FLAG" already defined near line 1 <<<
>>> /etc/sudoers.d/b: Alias "USER_FLAG" already defined near line 2 <<<
sudo: parse error in /etc/sudoers.d/b near line 1
sudo: no valid sudoers sources found, quitting
sudo: unable to initialize policy plugin
```

突然意识到了问题的严重性，我可能需要重启进入单用户模式才能解决。但不相重启于是网上搜索一下果然在StackExchange找到了一个解决方案，使用`pkexec`命令。于是执行`pkexec visudo /etc/sudoers.d/b`，在弹出的权限认证页面输入管理员账户密码便可正常编辑配置文件。

我使用的时VNC连接，原回答中说可以使用SSH登录后使用`pkexec`命令，但是我自己测试发现输入正确的密码后依然提示认证失败。同一个问题下面的另一个回答给出了一个使用`pkttyagent`的解决方法，例如下面的命令删除有问题的配置文件，该方法可以完成权限认证，但是可能会失去Shell的控制，即不能在当前Shell中输入命令，不过在我的测试中使用Ctrl+c可以恢复Shell的使用。

```sh
pkttyagent -p $(echo $$) | pkexec rm /etc/sudoers.d/FILENAME
```

该回答中还给出了另一个使用live CD的方法，当系统中没有可用的具有管理员权限的用户时，可以使用该方法或进入但用户模式修改。

1. [sudo - How to modify an invalid '/etc/sudoers' file? - Ask Ubuntu](https://askubuntu.com/questions/73864/how-to-modify-an-invalid-etc-sudoers-file)
