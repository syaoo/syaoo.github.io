---
title: screen使用（摘录）
tag: ['Linux','screen']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover1.jpg
---

摘录一些screen命令的使用技巧。使用screen可以在一个会话窗口运行多个程序，能够避免因会话中断而是正在运行的程序终止，有点类似于nohup与&配合效果。 

<!--more-->

## 命令参数
| 参数                              | 作用                                                         |
| --------------------------------- | ------------------------------------------------------------ |
| `-c file                         | 使用配置文件file，而不使用默认的$HOME/.screenrc`              |
| `-d -D [pid.tty.host]`|不开启新的screen会话，而是断开其他正在运行的screen会话|
| `-h num`                          | 指定历史回滚缓冲区大小为num行                                |
| ``-list|-ls``                     | 列出现有screen会话，格式为pid.tty.host                       |
| `-d -m`                           | 启动一个开始就处于断开模式的会话                             |
| `-r sessionowner/ [pid.tty.host]` | 重新连接一个断开的会话。多用户模式下连接到其他用户screen会话需要指定sessionowner，需要setuid-root权限 |
| `-S sessionname`                    | 创建screen会话时为会话指定一个名字                           |
| `-v`                                | 显示screen版本信息                                           |
| `-wipe [match]`                     | 同-list，但删掉那些无法连接的会话                            |

## 快捷键
| 快捷键   | 功能                                      |
| -------- | ----------------------------------------- |
| C-a ?    | 显示所有键绑定信息                        |
| C-a w    | 显示所有窗口列表                          |
| C-a C-a  | 切换到之前显示的窗口                      |
| C-a c    | 创建一个新的运行shell的窗口并切换到该窗口 |
| C-a n    | 切换到下一个窗口                          |
| C-a p    | 切换到前一个窗口(与C-a n相对)             |
| C-a 0..9 | 切换到窗口0..9                            |
| C-a a    | 发送 C-a到当前窗口                        |
| C-a d    | 暂时断开screen会话                        |
| C-a k    | 杀掉当前窗口                              |
| C-a [    | 进入拷贝/回滚模式                         |

---

**参考**
1. [linux 技巧：使用 screen 管理你的远程会话](https://www.ibm.com/developerworks/cn/linux/l-cn-screen/index.html)
