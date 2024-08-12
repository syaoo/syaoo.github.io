import re

def find_markdown_images(mdstr:str):
    """
    从 Markdown 字符串中提取图片地址
    
    参数:
    markdown_file (str) - Markdown 文件的路径
    
    返回:
    image_names (list) - 图片名称列表
    image_urls (list) - 图片地址列表
    """
    # 使用正则表达式匹配图片 Markdown 语法
    # pattern = r'!\[(.*?)\]\((.*?)\)' # 同时提取替代文件
    pattern = r'!\[.*\]\((.*?)\)'
    matches = re.findall(pattern, mdstr)
    return matches

def find_html_images(htmlstr:str):
    # 使用正则表达式匹配html图片
    pattern =r'<img\s+(?:[^>]*?\s+)?src="([^"]*)"'
    matches = re.findall(pattern, htmlstr)
    return matches

def test_markdown():
    mdstr = """
    <!--more-->

通常使用matplotlib绘图有隐式(pyplot-style)与显式(object-oriented (OO) style)两种：
 > 将pyplot-style使用在交互式绘图（如在Jupyter Notebook），OO-style用于非交互式绘图（如在函数或脚本中），对于复杂图像绘制推荐使用面向对象的API (OO-style)。[^1]

## 基础操作
如果使用pyplot-style方式绘图，操作同Matlab几乎一样的：
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

### 绘图函数
matplotlib可以内置许多绘图函数，[这里](https://matplotlib.org/api/axes_api.html#plotting)可以查看所有可用的图形类型，下面介绍用于绘制折线图、散点图、条形图、直方图、饼图、箱线图等图形的函数。
    """
    # 使用正则表达式匹配图片 Markdown 语法
    images = find_markdown_images(mdstr)
    
    print('Markdown Image:')
    for name in images:
        print(name)


def test_html():
    htmlstr = """
<!DOCTYPE html>
<html>
<body>
<div>
Hello!
</div>
<img alt="Smiley face" src="smiley1.gif"  width="44" height="42" style="border:5px solid black">123
<div>
Hello!
</div>
<img  src="smiley2.gif"  width="44" height="42" style="border:5px solid black">

<div>
Hello!
</div>
<a href="https://www.w3schools.com"><img alt="Smiley face" src="smiley3.gif"  width="44" height="42" style="border:5px solid black"></a>

</body>
</html>
    """
    images = find_html_images(htmlstr)
    
    print('HTML Image:')
    for name in images:
        print(name)

def load_markdown(filename:str):
    content=None
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def test_find():
    f="_posts/2021-09-17-ellip.md"
    c=load_markdown(f)
    i=find_markdown_images(c)
    j=find_html_images(c)
    
    print("markdown:")
    for m in i:
        print(m)
    print("html:")
    for m in j:
        print(m)
if __name__ == "__main__":
    # 示例使用
    test_markdown()
    test_html()
    test_find()
