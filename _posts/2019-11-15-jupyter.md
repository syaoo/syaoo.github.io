---
title: JupyterLab安装使用
tag: ["JupyterLab"]
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---
JupyterLab是一个基于Web的文档编辑工具，可以用来编辑Jupyter Notebook、文本文件、Markdown等，其具有丰富的功能，而且可以通过安装插件来扩展其功能。JupyertLab可以部署到服务器，在任意设备使用JupyterLab服务，可以将Notebook转换为HTML、Markdown、PDF、Latex等多种文件格式，而且还可以制作PPT，方便的展示编写的代码。
<!--more-->

## 安装及使用  
JupyterLab可是使用`conda`,`pip`,`pipenv`,`docker`安装。
本文使用`pip`安装：
```bash
pip3 install jupyterlab
```
输入`jupyter lab`即可启动Jupyter Lab并自动打开浏览器(推荐使用Firefox浏览器)
*ubuntu上如果出现找不到jupyter命令的情况，尝试注销账户后重新登陆*
## 配置  
### 生成并修改配置文件使其可以在远程访问。  
`jupyter lab --generate-config`生成一个配置文件，记下输出的配置文件地址
设置密码：
```bash
>>> from notebook.auth import passwd
>>> passwd()
Enter password:
Verify password:
'sha1:60649f10478f:d9c610c97d296d3ad7120a4efc2c80a3b27fb25f'
# 在这里输入想要设置的登录JupyterLab 的密码 然后会有一串输出，复制下来，等会配置需要使用
```

找到配置文件中下面这几行条目，取消注释并修改：
```bash
# 允许以root方式运行jupyterlab
c.NotebookApp.allow_root = True
# 允许任意ip段访问
c.NotebookApp.ip = '0.0.0.0'
# 设置jupyterlab页面的根目录
c.NotebookApp.notebook_dir = u'/root/JupyterLab'
# 默认运行时不启动浏览器
c.NotebookApp.open_browser = False 
# 设置之前生产的哈希密码
c.NotebookApp.password = u'sha1:60649f10478f:d9c610c97d296d3ad7120a4efc2c80a3b27fb25f' # 上面生成的密码sha1
# 设置访问端口
c.NotebookApp.port = 8080
# 启用mathjax
c.NotebookApp.enable_mathjax = True
```

### *使用 https*

## Notebook的使用
#### *Magic Code*  
以下摘自[码农网](https://www.codercto.com/a/75771.html)
IPython的一些特殊命令（不是内置于 Python 本身）被称为“魔术”命令。魔术命令是以百分号％为前缀的任何命令。

*%matplotlib*
最常用的魔法命令，大概就是 %matplotlib [10] 了。它用于指定 matplotlib 的后端(backend)。通常我们使用：
`%matplotlib inline`
代表使用 inline作为后端，直接在 Notebook 中内嵌图片，并且可以省略掉 plt.show() 这一步骤。
`％timeit` 函数检查任何 Python 语句的执行时间
你可以使用`%run`命令，在Notebook中运行任意的Python文件。例如：
`%run add.py`
还有其他一些常用命令，例如 `%debug`、`%load_ext` 和 `%pwd`等。  
### 使用系统命令
在cell中`!command`可以调用系统命令如`!ls`查看当前目录。

## 制作PPT  
使用JupyterLab可以轻松的制作网页版PPT。  
首先选中cell在左侧`Notebook Tools`选项中设置幻灯片类型(Slide Type)  
![JSBVxI.png](https://s1.ax1x.com/2020/04/14/JSBVxI.png)

有五种类型可选： 
- slide：一张新的幻灯片
- subslide：向下滑动的幻灯片
- fragment：一个片段，类似PPT的动画
- skip：不显示
- notes：备注 
设置完成后，可以从`File` - `Export Notebook As` - `Export Notebook to Reveal.js Slides`导出HTML文件，或者使用命令`jupyter nbconvert foo.ipynb --to slides`
命令`jupyter nbconvert foo.ipynb --to slides --post serve`会将Notebook转换为HTML文件，并从发布到本地服务器（如下图）。
![JSfbdA.png](https://s1.ax1x.com/2020/04/14/JSfbdA.png)

## 插件  
JupyterLab 的插件是 npm 安装包。所以按照 JupyterLab 的插件，需要提前按照好 Node.js。
`conda install -c conda-forge nodejs`  
*如果jupyterlab是通过conda安装的使用conda安装nodejs后就可以直接使用`jupyter labextension install ext-name`安装插件了;  
我设备上jupyterlab是使用apt安装的，在安装插件时会使用系统环境的nodejs，因此还需要在系统环境中使用apt安装nodejs和npm*  
查看已安装插件：`jupyter labextension list`  
更新已安装插件：`jupyter labextension update --all`  
菜单栏：setting->Enables extension manager启用插件管理，就可以在左侧工具栏看到插件图标，在这里可以安装、卸载管理插件。  
 jupyterlab-toc–生成目录:`jupyter labextension install @jupyterlab/toc`  
 Jupyterlab_voyager:Voyager是一种数据可视化工具，可以自动和手动的生成图表。用来查看数据的基本分布信息，十分方便。`jupyter labextension install jupyterlab_voyager
`  
Jupyterlab-drawio 是一个在绘图插件，它将drawio / mxgraph独立集成到了 jupyterlab 中。:`jupyter labextension install jupyterlab-drawio
`  
[lab 交互控件](https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html) `jupyter labextension install @jupyter-widgets/jupyterlab-manager`

[插件列表](https://github.com/topics/jupyterlab-extension)

## 其他语言支持
1. [R语言](https://github.com/IRkernel/IRkernel)  
CRAN中现在有这个包
```R
install.packages('IRkernel') # 安装IRkernel包
IRkernel::installspec()  # 注册当前R安装的内核使jupyterlab能够识别
```

参考  
[官方教程](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html)  
[云服务器搭建神器JupyterLab（多图）](https://zhuanlan.zhihu.com/p/48387217)  
[利器|JupyterLab 数据分析必备IDE完全指南 - 知乎](https://zhuanlan.zhihu.com/p/67959768)