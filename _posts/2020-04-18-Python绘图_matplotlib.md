---
title: Matplotlib - Python数据可视化
tag: ["Matplotlib", " Python"]
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover0.jpg
---

[Matplotlib](https://matplotlib.org/tutorials/index.html)是一个功能强大的数据可视化Python库，利用它可以绘制`折线图(plot)`, `柱形图( bar)`, `直方图(hist)`, `饼图(pie)`, `箱线图(box)`, `密度图(kde)`, `面积图(area)`, `(散点图 (scatter)`, `散点图矩阵(scatter_matrix)` 等。 通过matplotlib.pyplotlib子库可以方便的绘制各种图像，可以Matlab中绘图 那样方便。

<!--more-->

通常使用matplotlib绘图有隐式(pyplot-style)与显式(object-oriented (OO) style)两种，前者是在绘图时pyplot的函数会自动实例化并管理Figure、Axes等Matplotlib可视化类，后者则需要用户创建方法Figure以及Axes类，然后通过对可视化类的操作来绘图。一般在程序性使用什么方式并没有明确的要求，可以使用某一种，甚至可以混用，在官方文档中给的建议是：
 > 将pyplot-style使用在交互式绘图（如在Jupyter Notebook），OO-style用于非交互式绘图（如在函数或脚本中），对于复杂图像绘制推荐使用面向对象的API (OO-style)。[^1]

## 基础操作
如果使用pyplot-style方式绘图，操作同Matlab几乎一样的。比如绘制一段正弦曲线：
 示例1、matplotlib.pyplot绘图:

 ```python
 import numpy as np
 import matplotlib.pyplot as plt
 import matplotlib as mpl
 
 x = np.linspace(-2*np.pi,2*np.pi,100)
 y = np.sin(x)
 
 fig=plt.figure(num='图1')
 plt.plot(x,y,label='sin(x)')
 plt.legend()
 plt.title('y=sin(x)')
 plt.xlabel('x')
 plt.ylabel('y')
 plt.show()
 ```
 输出效果
 ![JVWnUK.png](https://s1.ax1x.com/2020/04/17/JVWnUK.png)

 示例2、Matlab绘图：
 ```matlab
 x=linspace(-2*pi,2*pi,100);
 y=sin(x)
 fig=figure('Name','图1');
 plot(x,y)
 legend('sin(x)')
 title('y=sin(x)')
 xlabel('x')
 ylabel('y')
 ```
![JVWmE6.png](https://s1.ax1x.com/2020/04/17/JVWmE6.png)

在pyplot-sytle中使用`plt.plot()`时自动创建了Figure、Axes，后面的操作都是针对当前Figure(gcf)，当前Axes(gca)操作；对于OO-style,也就是面向对像的方式，需要先实例化Figure以及Axes才能在Axes上绘图。
 下面代码是OO-Style,绘图效果与pyplot-style相同
 实例3、面向对象的绘图方式
 ```python
 fig,ax=plt.subplots() # 创建一个Figure并添加一个Axes
 # # 或者
 # fig = plt.figure()
 # ax = fig.add_subplot()
 ax.plot(x,y,label='sin(x)')
 ax.legend()
 ax.set_title('y=sin(x)')
 ax.set_xlabel('x')
 ax.set_ylabel('y')
 fig.show()
 plt.show() # 在脚本中使用fig.show()图像不能停留
 ```
两种方式添加绘图区添加title、label等元素的方式有所不同，前者是使用pyplot的函数(如`plt.title()`)，而后者是使用类的方法(`ax.set_title()`),二者函数明不同但是使用的参数是相同的。

### 绘图函数
matplotlib可以内置许多绘图函数，[这里](https://matplotlib.org/api/axes_api.html#plotting)可以查看所有可用的图形类型，下面介绍用于绘制折线图、散点图、条形图、直方图、饼图、箱线图等图形的函数。

所有绘图函数都将`numpy.array`或`numpy.ma.masked_array`作为输入。“array-like”类型（如pandas数据对象和numpy.matrix）不一定能正常使用。最好将其转换为`numpy.array`对象。

#### [plot](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html#matplotlib.axes.Axes.plot)
通常用于绘制折线图，如示例1中使用的方式，plot函数的调用格式：
 ```python
 plot([x], y, [fmt], *, data=None, **kwargs)
 plot([x], y, [fmt], [x2], y2, [fmt2], ..., **kwargs)
 ```
 fmt是格式字符串，有三个字符表示线型(linestyle or ls)、标记点样式(marker)、颜色(color or c)的简化方式：`fmt = '[marker][line][color]'`
 marker, line,color的可选值

| marker | 标记         | color | 颜色          | line   | 线型   |
| ------ | ------------ | ----- | ------------- | ------ | ------ |
| `'.'`  | 点           | `'b'` | 蓝色(blue)    | `'-'`  | 实线   |
| `','`  | 像素点       | `'g'` | 绿色(green)   | `'--'` | 虚线   |
| `'o'`  | 圆圈         | `'r'` | 红色(red)     | `'-.'` | 点划线 |
| `'v'`  | 下三角       | `'c'` | 青色(cyan)    | `':'`  | 点线   |
| `'^'`  | 上三角       | `'m'` | 品红(magenta) |        |        |
| `'<'`  | 左三角       | `'y'` | 黄色(yellow)  |        |        |
| `'>'`  | 右三角       | `'k'` | 黑色(black)   |        |        |
| `'1'`  | tri_down     | `'w'` | 白色(white)   |        |        |
| `'2'`  | tri_up       |       |               |        |        |
| `'3'`  | tri_left     |       |               |        |        |
| `'4'`  | tri_right    |       |               |        |        |
| `'s'`  | square       |       |               |        |        |
| `'p'`  | pentagon     |       |               |        |        |
| `'*'`  | star         |       |               |        |        |
| `'h'`  | hexagon1     |       |               |        |        |
| `'H'`  | hexagon2     |       |               |        |        |
| `'+'`  | plus         |       |               |        |        |
| `'x'`  | x            |       |               |        |        |
| `'D'`  | diamond      |       |               |        |        |
| `'d'`  | thin_diamond |       |               |        |        |
| `'|'`  | vline        |       |               |        |        |
| `'_'`  | hline        |       |               |        |        |

*更多[marker](https://matplotlib.org/api/markers_api.html#module-matplotlib.markers)*，对于颜色，除了上面的颜色字符外，还可以使用rgb元组`(R,G,B)`等方式指定。    
其他更多属性(alpha, linewidth等)设置，详见[matplotlib.lines.Line2D](https://matplotlib.org/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D)。也使用plt.setp()可以查询、设置属性
 ```python
 theline = plt.plot(x,y)
 print(plt.setp(theline)) # 输出theline的属性
 plt.setp(l1,color='r') # 设置theline的颜色为红色
 ```

#### [scatter](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.scatter.html#matplotlib.axes.Axes.scatter)
虽然plot可以使用`'.'`标记绘制简单的散点图，但scatter可以实现更丰富的效果，表达更多维度的信息。相比与plot，scatter还有与x,y元素数相同的s,c参数用于指定标记点的大小与颜色。此外还有marker用于指定标记点、alpha透明度等参数,
 示例4、自定义标记形状的散点图
 ```python
 import matplotlib.pyplot as plt
 import numpy as np
 
 # unit area ellipse
 rx, ry = 3., 1.
 area = rx * ry * np.pi
 theta = np.arange(0, 2 * np.pi + 0.01, 0.1)
 verts = np.column_stack([rx / area * np.cos(theta), ry / area * np.sin(theta)]) # 椭圆路径
 
 x, y, s, c = np.random.rand(4, 30)
 s *= 10**2.
 
 fig, ax = plt.subplots()
 ax.scatter(x, y, s, c, marker=verts)
 
 plt.show()
 ```
 ![JZcnxA.png](https://s1.ax1x.com/2020/04/17/JZcnxA.png)

#### 条形图
[bar](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.bar.html#matplotlib.axes.Axes.bar)用于绘图条形图，[barh](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.barh.html#matplotlib.axes.Axes.barh)可以绘制横向条形图;二者区别仅前三个参数不同：
 ```python
 plt.bar(x,height,width=0.8) # 条形图
 plt.barh(y, width,height=0.8) # 横版条形图
 ```
 示例5、带有误差线的累积条形图
 ```python
 import numpy as np
 import matplotlib.pyplot as plt
 
 
 labels = ['G1', 'G2', 'G3', 'G4', 'G5']
 men_means = [20, 35, 30, 35, 27]
 women_means = [25, 32, 34, 20, 25]
 men_std = [2, 3, 4, 1, 2]
 women_std = [3, 5, 2, 3, 3]
 width = 0.35       # 条带的宽度: 也可是长度为len(x)的序列
 
 fig, ax = plt.subplots()
 ax.bar(labels, men_means, width, yerr=men_std, label='Men')
 ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
        label='Women')
 
 ax.set_ylabel('Scores')
 ax.set_title('Scores by group and gender')
 ax.legend() 
 plt.show()
 ```

#### [hist](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.hist.html#matplotlib.axes.Axes.hist)
直方图通常用于表示连续数据的分布情况，在Matplotlib中hist用于绘制条形图，同时还会返回直方图中每个分组的数量及分组的边界。`bins`参数控制分组数量或者定义分组，`density`参数指定是否将统计结果归一化，`color`指定直方图颜色(一组数据一种颜色)，更多参数可以查看官方文档。此外使用bar也可实现直方图的效果
 示例6、直方图示例
 ```python
  import random
 random.seed(1000)
 x=np.random.randn(1000,2)
 
 fig, ax = plt.subplots(2,2)
 fig.set_size_inches(10,10) # 设置图像大小
 
 ax[0,0].hist(x,bins=10,label=['data1','data2'])
 ax[0,0].legend()
 ax[0,0].set_title('10 groups')
 
 bins = [-3,-2,-1,0,1,2,3]
 ax[0,1].hist(x,bins=bins,label=['data1','data2'],density=True)
 ax[0,1].legend()
 ax[0,1].set_title('Use sequence grouping')
 # od=np.histogram(x[:,1])
 # plt.bar(od[1][:-1],od[0],align='edge')
 
 ax[1,0].hist(x,bins=bins,label=['data1','data2'],density=True,stacked=True)
 ax[1,0].legend()
 ax[1,0].set_title('Stack groups of data')
 
 hdat0 = np.histogram(x[:,0],bins=bins,density=True)
 hdat1 = np.histogram(x[:,1],bins=bins,density=True)
 ax[1,1].bar(hdat0[1][:-1],hdat0[0],align='edge',width=1,label='data1')
 ax[1,1].bar(hdat1[1][:-1],hdat1[0],bottom=hdat0[0],align='edge',width=1,label='data2')
 ax[1,1].legend()
 ax[1,1].set_title('use bar funtion')
 plt.show()
 ```
 [![JedeS0.png](https://s1.ax1x.com/2020/04/18/JedeS0.png)](https://imgchr.com/i/JedeS0)

此外还有`hist2d`可以绘制双变量直方图。

#### [pie](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.pie.html#matplotlib.axes.Axes.pie)
pie用于绘制饼图，并返回饼图表示各部分标签及百分比的Text类列表，`patches, texts, autotexts=pie(x, explode=None, labels=None, colors=None)`当`sum(x)<1`时，会把x中各元素当作百分比，且缺失的部分在饼图中显示为空白，explode参数指定各部分的偏移量，labels指定各部分标签，color指定颜色。
 示例7、分离式饼图
 ```python
 # 饼图，按逆时针方向排列和绘制
 labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
 sizes = [15, 30, 45, 10]
 explode = (0, 0.1, 0, 0)  # 只分离'Hogs'
 
 fig1, ax1 = plt.subplots()
 ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
         shadow=True, startangle=90)
 ax1.axis('equal')  # 等比例坐标轴，确保将饼图绘制为圆。
 plt.show()
 ```
 ![JeDUCd.png](https://s1.ax1x.com/2020/04/18/JeDUCd.png)

#### [boxplot](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.boxplot.html#matplotlib.axes.Axes.boxplot)
boxplot用于绘制箱线图，会返回一个包含boxes、medians、whiskers、caps
、fliers、means的字典。箱线图主要中包含数据的上边缘值、上四分位数、中位数、下四分位数、下边缘值及异常值，可以通过设置对于参数来做相应的处理。
 示例8、自定义颜色的箱线图
 ```python
 np.random.seed(19680801)
 all_data = [np.random.normal(0, std, size=100) for std in range(1, 4)]
 labels = ['x1', 'x2', 'x3']
 
 fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
 
 # 矩形 box plot
 bplot1 = ax1.boxplot(all_data,
                      vert=True,  # vertical box alignment
                      patch_artist=True,  # fill with color
                      labels=labels)  # will be used to label x-ticks
 ax1.set_title('Rectangular box plot')
 
 # 有缺口 box plot
 bplot2 = ax2.boxplot(all_data,
                      notch=True,  # notch shape
                      vert=True,  # vertical box alignment
                      patch_artist=True,  # fill with color
                      labels=labels)  # will be used to label x-ticks
 ax2.set_title('Notched box plot')
 
 # 填充颜色
 colors = ['pink', 'lightblue', 'lightgreen']
 for bplot in (bplot1, bplot2):
     for patch, color in zip(bplot['boxes'], colors):
         patch.set_facecolor(color)
 
 # 添加横向网格线
 for ax in [ax1, ax2]:
     ax.yaxis.grid(True)
     ax.set_xlabel('Three separate samples')
     ax.set_ylabel('Observed values')
 
 plt.show()
 ```
 [![JmA0S0.png](https://s1.ax1x.com/2020/04/18/JmA0S0.png)](https://imgchr.com/i/JmA0S0)

#### 其他绘图函数
除了上面介绍的较为常用的绘图函数外，matplotlib还有polar、psd()、specgram()、cohere()、step()等更多绘图函数。

### 样式设置
通常个函数画出图像后会有一个默认的样式，matplotlib有多种[内置样式](https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html)，可以使用`matplotlib.style.available`查看可用样式，使用`matplotlib.style.use('样式名')`修改默认样式。当然，默认样式通常不能满足需要，为让图像能更好的传达信息，让图像更美观，还需要对图表样式做一定的调整。
#### 网格、图例、标题，轴标签
1. [grid](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.grid.html?highlight=grid#matplotlib.axes.Axes.grid)  
`grid( b=None, which='major', axis='both', |*|*kwargs)`控制坐标网格的显示及样式，当所有参数缺省时表示切换网格的可见性。which：{'major', 'minor', 'both'}指定网格类型主网格、副网格或者二者都有，axis：{'both', 'x', 'y'}指定x、y轴方向的网格。其他参数color,linestyle, linewidth等。
2. legend([Axes.legend](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.legend.html?highlight=legend#matplotlib.axes.Axes.legend),[pyplot.legend](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html?highlight=legend#matplotlib.pyplot.legend)),[Figure.legend](https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html?highlight=legend#matplotlib.figure.Figure.legend)  
Axes.legend是在该Axes上显示图例，第二个是在当前Axes上显示图例，最后一个是在该Figure上显示图例，可指定参数设置字体大小fontsize等属性或使用setp修改、查询。  
有三种调用方式：1、`legend()`,2、`legend(labels)`,3、`legend(handles, labels)`，方式1、显示已有的legend元素（即label参数的值），如果没有则不能正常显示，
示例9、图例的显示
    ```python
    fig,((ax1,ax2),(ax3,ax4))= plt.subplots(2,2,figsize=(10,10))
    x = np.linspace(0,10,20)
    y=np.sin(x)
    y1=np.cos(x)
    
    ax1.plot(x,y,'o-',x,y1,'x-')
    ax1.legend(['sin(x)','cos(x)'])
    
    lins = ax2.plot(x,y+1,'+-',x,y1+1,'*-')
    ax2.legend(lins,['cos(x)+1','sin(x)+1'])
    
    lins = ax3.plot(x,y+1,'y1-',x,y1+1,'k*-',label=['sin(x)+1(y)','cos(x)+1(k)'])
    ax3.legend(loc='best')
    
    plt.plot([1,2,3,5])
    ax4.legend(['line'])
    
    fig.legend(['1','2','3','4'])
    ```
    ![JmC90A.png](https://s1.ax1x.com/2020/04/18/JmC90A.png)
   
3. 标题
Axes、Figure、legend等都有标题，设置方法也很多，如Axes标题`plt.title('str')`(作用与当前Axes),`Axes.set_title('str')`以及使用`setp`函数。Figure的标题可以使用`plt.suptitle('str')`,`fig.suptitle('str')`,legend标题可以使用`legend(title='str')`,`legend.set_title('set')`以及setp设置标题。
4. xlable,ylabel
坐标轴的标题，可通过`plt.xlabel('str')`,`plt.ylabel('str')`,`Axes.set_xlabel('str')`,`Axes.set_ylabel('str')`等方式设置。

#### 坐标轴样式
matplotlib除了常规坐线性标轴外，还支持对数、时间序列等坐标轴，还有极坐标等其他不同投影方式的坐标系。
1. 对数轴  
当数据跨越多个量级时，通常使用对数轴，在matplotlib中可以使用`plt.xsacle('log')`设置x轴为对数轴，还有`Axes.set_xsacle('log')`,`'log'`表示对数轴，`'linear'`表示线性轴，`'symlog'`、`'logit'`为其他形式的对数轴。`yscale`,`set_yscale`作用与y轴。
2. 时间序列
plot_date
https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot_date.html#matplotlib.axes.Axes.plot_date
https://blog.csdn.net/helunqu2017/article/details/78736686
3. 投影

#### 其他文本（图例、注释等）
text任意位置文本,annotate带箭头注释）


### 多Figure、多Axes布局
 See Axes Demo for an example of placing axes manually and Basic Subplot Demo for an example with lots of subplots.

https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots.html#matplotlib.pyplot.subplots
子图
多个坐标区域subplot
subplot2grid( ), gridspec类 gridspec.Gridspec(3,3) ax1=plt.subplot(gs[0,:])


## 中文字体显示
Matplotlib本身并不支持中文字体的显示，若要正常显示中文字体需要进行一些设置，通常有两种方法：
1. 局部设置，在需要时指定字体  
   ```python
   # 这个方向指定的字体必须是系统存在的字体
   plt.xlabel('时间',fontproperties='SimHei') # 设置x轴标签的字体
   # 使用font_manager通过字体文件指定字体
   font_path = './songti.ttf'
   _font = mpl.font_manager.FontProperties(fname=font_path)
   plt.xlabel('时间',fontproperties=_font)
   ```
2. 全局设置，当前程序中所有图形字体  
`matplotlib.rc()`用于设置当前rc参数，通过它可以设置字体的参数
   ```python
   ## 以下3种写法效果相同
   font = {'family' : 'monospace',
          'weight' : 'bold',
          'size'   : 15}
   matplotlib.rc('font', **font)  # 通过字典传入参数
   #  关键字传参
   matplotlib.rc('font', family='monospace',weight='bold',size=15)
   # 修改rcParams
   matplolib.rcParams['font.family']='monospace'
   matplolib.rcParams['font.weight']='bold'
   matplolib.rcParams['font.size']=15
   ```
   family：字体名称；font.style：字体风格，如 'normal','itaic'；font.size 字体大小。
    一些常见字体：

    字体|说明
    -|-
    SimHei|黑体
    Kaiti|楷体
    LiSu|隶书
    FangSong|仿宋
    YouYuan|幼圆
    STSong|宋体



其他绘图工具:    
- [Seaborn](http://seaborn.pydata.org/): Seaborn是一个基于matplotlib的Python数据可视化库。它提供易于使用的高级接口，可以方便绘制`概率分布图(displot )`,  `密度分布图(kdeplot)`, `联合分布图(joinplot)`, `箱线图(boxplots)`, `回归图(lmplot)`, `热力图( heatmap)`等许多信息丰富的图形；
- [altair](https://altair-viz.github.io/): Declarative statistical visualization library for Python;     
- [`plotly`](https://plotly.com/python/getting-started/#initialization-for-offline-plotting): plotly是一个交互式的开源绘图库，它支持40多种独特的图表类型;  
- [Echart](https://www.echartsjs.com/zh/index.html): 使用JavaScript实现的开源数据可视化框架，Python可以通过模块[`pyecharts`](http://pyecharts.org/#/)来调用Echart。  

---

参考：  
[Pyplot tutorial — Matplotlib 3.2.1 documentation:](https://matplotlib.org/tutorials/introductory/pyplot.html#sphx-glr-tutorials-introductory-pyplot-py)  
[Python 数据分析与展示(北京理工大学 )](https://www.bilibili.com/video/BV1Sx411U7R9)  
[Python数据可视化分析 matplotlib教程](https://www.bilibili.com/video/av6989413)  


Python+Matplotlib制作动画 - EndlessCoding - 博客园: https://www.cnblogs.com/endlesscoding/p/10308111.html

^[1]: [Usage Guide — Matplotlib 3.2.1 documentation](https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py)
