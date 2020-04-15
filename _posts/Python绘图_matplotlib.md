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

[Matplotlib](https://matplotlib.org/tutorials/index.html)是一个功能强大的数据可视化Python库，该库让使用Python像在Matlab中那样方便。利用它可以绘制`折线图(plot)`, `柱形图( bar)`, `直方图(hist)`, `饼图(pie)`, `箱线图(box)`, `密度图(kde)`, `面积图(area)`, `(散点图 (scatter)`, `散点图矩阵(scatter_matrix)` 等。 

<!--more-->
Matlabplot图形主要有Figure、Axes、Axis、Artist四个主要部分，Figure是Axes、Axis以及Artist等元素的容器；Axes是具体的绘图区域，可以包含多个Axis；Axis就是坐标轴；图中所有可见元素都是Artist，如Legned, Lines,甚至Figure, Axes, Axis，下图标注了完整Matplotlib图形的各元素名称：
![GphsFe.png](https://s1.ax1x.com/2020/03/26/GphsFe.png)  

## Figure

## Axes
## Axis
## Artist

其他绘图工具:    
- [Seaborn](http://seaborn.pydata.org/): Seaborn是一个基于matplotlib的Python数据可视化库。它提供易于使用的高级接口，可以方便绘制`概率分布图(displot )`,  `密度分布图(kdeplot)`, `联合分布图(joinplot)`, `箱线图(boxplots)`, `回归图(lmplot)`, `热力图( heatmap)`等许多信息丰富的图形；
- [altair](https://altair-viz.github.io/): Declarative statistical visualization library for Python;     
- [`plotly`](https://plotly.com/python/getting-started/#initialization-for-offline-plotting): plotly是一个交互式的开源绘图库，它支持40多种独特的图表类型;  
- [Echart](https://www.echartsjs.com/zh/index.html): 使用JavaScript实现的开源数据可视化框架，Python可以通过模块[`pyecharts`](http://pyecharts.org/#/)来调用Echart。  

Python+Matplotlib制作动画 - EndlessCoding - 博客园: https://www.cnblogs.com/endlesscoding/p/10308111.html