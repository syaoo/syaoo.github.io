---
title: Streamlit - Python Web应用框架
tag: Streamlit
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---

> Streamlit是一个开放源代码的Python库，可以轻松地为机器学习和数据科学构建漂亮的自定义web应用程序。  

特点：简单易用，能够轻松**缓存数据**，不用在每次运行程序时都重复加载数据，提升运行效率。
<!--more-->

## 安装Streamlit

> 环境要求：Python 2.7.0 or later / Python 3.6.x or later；为避免Streamlit的依赖项与其他工作环境相冲突，最好使用conda等创建虚拟环境安装。

1. 使用pip安装  

    ```bash
    pip install streamlit
    ```

2. 测试是否可以正常工作  
输入下面的命令进行测试

    ```bash
    streamlit hello
    ```

3. 常用命令  

    ```bash
     streamlit --help # 命令介绍
     streamlit config show # 显示配置信息
    ```

    可以看到如下的输出，同时浏览器会自动打开测试页面，里面有四个演示程序：

    ```bash
    You can now view your Streamlit app in your browser.
    Local URL: http://localhost:8501
    Network URL: http://192.168.0.104:8501
    ```

    ![86fPpj.png](https://s1.ax1x.com/2020/03/20/86fPpj.png)
    

[**演示程序**](/assets/code/StreamlitTest.py)

## 使用入门

1. 创建Python脚本  
创建一个名为`uber_pickups.py`的文件，导入streamlit：

    ```python
    import streamlit as st
    ```

2. 运行程序  
使用下面的命令运行程序,:

    ```bash
    streamlit run uber_pickups.py
    ```

    此时，可以在浏览器看到一个空白的页面。

3. 添加内容  
编辑python文件，先添加标题：  

    ```python
    st.title('Uber pickups in NYC')
    ```
   
    保存文件，可以看到之前打开的网页右上角提示文件改变，你可以选择`Rerun`重新运行程序，或者`Always rerun`文件保存后自动重新运行程序
    [![86heKI.png](https://s1.ax1x.com/2020/03/20/86heKI.png)](https://imgchr.com/i/86heKI)  
    重新运行后，网页标题就变成了`Uber pickups in NYC`.  

    之后，就可以按需要向里面添加文本，图标，以及streamlit控件等内容了。

## API介绍

1. Magic Commands(只能工作在Python3环境)  
Steamlit会自动将每行的变量或文本自动使用`st.write()`方式显示到程序中,其中文本支持MarkDown。同时它会自动忽略文件、函数开头的说明文本。[官方文档](https://docs.streamlit.io/api.html#magic-commands)示例代码

    ```python
    # Draw a title and some text to the app:
    # 下面第一行 等价 st.title('This is the document title')
    # 第二行 等价 st.write('This is some _markdown_.')
    '''
    # This is the document title

    This is some _markdown_.
    '''

    df = pd.DataFrame({'col1': [1,2,3]})
    df  # <-- Draw the dataframe

    x = 10
    'x', x  # <-- Draw the string 'x' and then the value of x
    ```

    也可以在配置文件`~/.streamlit/config.toml`中关闭Magic Commands

    ```toml
    [Convertingrunner]
    magicEnabled = false
    ```

1. 文本显示  
`st.title()`可以设置APP的标题,此外还有两个标题级别可以使用`st.header`和`st.subheader`.  
其他文本函数：  
`st.write`: 被称为瑞士军刀，可以自动显示多种数据类型，文本，变量，甚至图表等。
`st.text()`: 纯文本  
`st.markdown()`: Markdown(Github-flavored Markdow)  
`st.code()`  
`st.latex()`...  


3. 显示数据  
`st.writ()`自动格式化显示各种数据；  
`st.dataframe()`以交互的方式显示DataFrame；  
`st.table()`显示静态表格（将表格全部显示）；  
`st.json`将对象或字符串显示格式化的JSON字符串。  

4. 显示图表  
Streamlit支持Matplotlib、交互式图表[Vega Lite](https://vega.github.io/vega-lite/) (2D charts)和[deck.gl](https://github.com/uber/deck.gl) (maps and 3D charts)等图表库，同时Streamlit有一些“原生”绘图方式, 可以方便的绘制多种图表：  
用到的一些制图库：  
`matplotlib`,`Altair`,`Vega-Lite`,`Plotly`,`Bokeh`,`PyDeck`,`Deck.GL`,`dagre-d3`,
   
    ```python
    # 折线图
    line_chart(data=None, width=0, height=0, use_container_width=True)
    # 面积图
    area_chart(data=None, width=0, height=0, use_container_width=True)
    # 条形图
    bar_chart(data=None, width=0, height=0, use_container_width=True)
    # 显示matplotlib.pyplot图表
    streamlit.pyplot(fig=None, clear_figure=True, **kwargs)
    # 使用Altair库显示图表
    streamlit.altair_chart(altair_chart, use_container_width=False)
    # 使用Vega-Lite绘图
    vega_lite_chart(data=None, spec=None,use_container_width=False, **kwargs)
    # 显示交互式Plotly图表
    plotly_chart(figure_or_data, use_container_width=False, sharing='streamlit', **kwargs)
    # 显示交互式Bokeh chart.
    streamlit.bokeh_chart(figure, use_container_width=False)
    # PyDeck library，支持3D地图，点云等
    streamlit.pydeck_chart(pydeck_obj=None)
    # Deck.GL library 绘制地图
    streamlit.deck_gl_chart(spec=None, **kwargs)
    # dagre-d3 library.
    streamlit.graphviz_chart(figure_or_dot, width=0, height=0)
    # 将坐标点显示到地图上
    streamlit.map(data=None, zoom=None)
    ```

5. 多媒体  
嵌入图片、音频、视频文件

    ```python
    streamlit.image(image, caption=None, width=None, use_column_width=False, clamp=False, channels='RGB', format='JPEG')
    streamlit.audio(data, format='audio/wav', start_time=0)
    streamlit.video(data, format='video/mp4', start_time=0)
    ```

6. 控件  

    ```python
    # 返回按钮是否被点击T/F
    streamlit.button(label, key=None)
    # 返回复选框是否被选中
    streamlit.checkbox(label, value=False, key=None)
    # 返回选择的值
    streamlit.radio(label, options, index=0, format_func=<class 'str'>, key=None)
    # 单选返回选择值
    streamlit.selectbox(label, options, index=0, format_func=<class 'str'>, key=None)
    # 多选返回选择值列表
    streamlit.multiselect(label, options, default=None, format_func=<class 'str'>, key=None)
    # 返回一个数值或者数值元组(区间)int/float or tuple of int/float
    streamlit.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None)
    # 文本输入框,返回文本框中的字符串
    streamlit.text_input(label, value='', key=None, type='default')
    # 数值输入框，返回当前输入框的值
    streamlit.number_input(label, min_value=None, max_value=None, value=<streamlit.DeltaGenerator.NoValue object>, step=None, format=None, key=None)
    # 多行文本输入
    streamlit.text_area(label, value='', key=None)
    # 日期输入，返回datetime.date
    streamlit.date_input(label, value=None, key=None)
    # 时间输入、返回datetime.time
    streamlit.time_input(label, value=None, key=None)
    # 上传文件，返回BytesIO or StringIO or None
    streamlit.file_uploader(label, type=None, encoding='auto', key=None)
    ```

7. 侧边框  
`st.sidebar.[element_name]`不支持`st.write` (可以使用`st.markdown`替代) `st.echo`, and `st.spinner`.

8. 代码  

    ```python
     with st.echo():
         #这个块内的代码会被显示在APP
    ```

9. 进度及状态  

    ```python
    # 进度条
    streamlit.progress(value)
    # 执行代码块时临时显示消息。
    streamlit.spinner(text='In progress...')
    # Draw celebratory balloons.
    streamlit.balloons()
    # 显示错误信息
    streamlit.error(body)
    # 显示讲稿信息
    streamlit.warning(body)
    # 提示消息
    streamlit.info(body)
    # 成功信息
    streamlit.success(body)
    # 显示异常信息
    streamlit.exception(exception, exception_traceback=None)
    ```

10. 占位符、帮助、设置  

    ```python
    # 创建占位符
    streamlit.empty()
    # 显示帮助文档
    streamlit.help(obj)
    # 获取Steamlit的配置信息,返回指定选项的值
    # 使用streamlit config show命令查看详细配置项
    streamlit.get_option(key)
    # 修改配置, 目前只有client.caching, client.displayEnabled可在脚本中设置。
    streamlit.set_option(key, value)
    ```

11. 修改数据(Mutate data)  
    Streamlit可以修改已有元素（chart、table、DataFrame）的数据。
    ```python
    # 将数据添加到已有元素的数据底部
    DeltaGenerator.add_rows(data=None, **kwargs)
    ```

12. 性能优化-缓存数据  
`streamlit.cache(func=None, persist=False, allow_output_mutation=False, show_spinner=True, suppress_st_warning=False, hash_funcs=None, ignore_hash=False)`  
在函数定义前添加`@st.cache()`可以让Steamlit自动缓存函数的输出，避免每次运行时重复加载相同的数据，提升运行效率。 
Strealit每次执行被`@st.cache()`标记的函数是会做以下三件事：
    - 函数名字
    - 函数主体的代码
    - 函数输入参数  
第一次执行时，会将返回值保存到缓存中，之后调用该函数时如果上面三项保持不变则不在执行该函数，直接使用第一次缓存的结果。

    ```python
    @st.cache
    def fetch_and_clean_data(url):
        # Fetch data from URL here, and then clean it up.
        return data
    d1 = fetch_and_clean_data(DATA_URL_1)
    # Actually executes the function, since this is the first time it was
    # encountered.
    
    d2 = fetch_and_clean_data(DATA_URL_1)
    # Does not execute the function. Just returns its previously computed
    # value. This means that now the data in d1 is the same as in d2.
    d3 = fetch_and_clean_data(DATA_URL_2)
    # This is a different URL, so the function executes.
    ```

参考: [官方文档](https://docs.streamlit.io)