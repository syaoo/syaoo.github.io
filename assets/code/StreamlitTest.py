
def content(show_code):
    import streamlit as st
    import numpy as np
    st.sidebar.success("请在下拉列表选择项目")
    """
    该APP中包含两个项目, 内容均参考[官方文档](https://docs.streamlit.io/)：
    - [API](https://docs.streamlit.io/api.html#)测试项目,包括：  
        * Magic commands
        * Display text
        * Display data
        * Display charts
        * Display media
        * Display interactive widgets
        * Add widgets to sidebar
        * Display code
        * Display progress and status
        * Placeholders, help, and options
        * Mutate data
        * Optimize performance 
    - 实例演示  
        *  [Create a data explorer app](https://docs.streamlit.io/tutorial/create_a_data_explorer_app.html)
    """
    st.write("动画效果测试")
    import time
    progress_bar = st.progress(0)
    status_text = st.empty()
    chart = st.line_chart(np.random.randn(10, 2))

    for i in range(100):
        # Update progress bar.
        progress_bar.progress(i+1)
        new_rows = np.random.randn(10, 2)
        # Update status text.
        status_text.text(
            'The latest random number is: %s' % new_rows[-1, 1])
        # Append data to the chart.
        chart.add_rows(new_rows)

        # Pretend we're doing some computation that takes time.
        time.sleep(0.1)

    status_text.text('Done!')
    st.balloons()

def procUber():
    import numpy as np
    import pandas as pd

    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
    # 声明缓存该函数的输出 
    @st.cache
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data
    
    # 复选框来选择是否显示原始数据
    side_checkbox = st.sidebar.checkbox('Show raw data')
    # 动态时间；min: 0h, max: 23h, default: 17h 
    hour_to_filter = st.sidebar.slider('hour', 0, 23, 17)

    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    data = load_data(10000)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text('Loading data...done!')
    st.write('Done! (using st.cache)')
    # 如果勾选Show raw data 复选框，则以表格形式显示原始数据
    if side_checkbox:
        st.subheader('Raw data')
        st.write(data)

    # 使用steamlit原生方式绘制条形图，同时其也支持其他绘图包 Altair, Bokeh, Plotly, Matplotlib ... 
    st.subheader('Number of pickups by hour')
    hist_values = np.histogram(
        data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
    st.bar_chart(hist_values)

    # 将数据显示到地图上，其他方式：如: st.deckgl_chart
    st.subheader('Map of all pickups')
    st.map(data)
    # 通过滑块控制时间选择
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    st.subheader(f'Map of all pickups at {hour_to_filter}:00')
    st.map(filtered_data)

def uber(show_code):
    import inspect,textwrap
    import streamlit as st
    procUber()
    if  show_code:
        code,_ = inspect.getsourcelines(procUber)
        code = textwrap.dedent("".join(code[1:]))
        st.write('## 代码')
        st.code(code)

## API学习测试函数
import streamlit as st
import numpy as np
import pandas as pd
def testMgic():
    st.text("显示效果")
    # Magic commands 代码
    """
    # 这是标题 st.title()
    ## 这是次标题 st.subheader()
    这是正文 st.write()
    下面是表格：

    a|b
    -|-
    1|2
    2|4
    """
    df = pd.DataFrame({'col1': [1,2,3]})
    df  # <-- 显示DataFram

    x = 10
    'x', x  # <-- Draw the string 'x' and then the value of x

def testText():
    import altair as alt
    # 显示固定宽度的格式化字符串
    st.text('This is some text.')
    # streamlit.markdown(body, unsafe_allow_html=False)
    # 以Markdown格式显示字符串
    st.markdown('Streamlit is **_really_ cool**.')
    # 以Latex格式显示公式
    st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')

    # streamlit.write(*args, **kwargs)
    # 显示参数到APP，瑞士军刀般的命令，几乎可以自动化输出任何类型的数据
    st.write('Hello, *World!* :sunglasses:')
    st.write(1234)
    st.write(pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40],
    }))
    st.write('1 + 1 = ', 2)
    # 显示图表
    df = pd.DataFrame(np.random.randn(200, 3),
    columns=['a', 'b', 'c'])

    c = alt.Chart(df).mark_circle().encode(
        x='a', y='b', size='c', color='c')

    st.write(c)
    # streamlit.code(body, language='python')
    # 格式化显示代码
    code = '''def hello():
    print("Hello, Streamlit!")'''
    st.code(code, language='python')

def testDat():
    # streamlit.dataframe(data=None, width=None, height=None)
    df = pd.DataFrame(np.random.randn(30, 10),columns=('col %d' % i for i in range(10)))
    st.dataframe(df,500,100)  # 与st.write(df)相同
    # 利用Pands Style类修改df样式
    st.dataframe(df.style.highlight_max(axis=0),height=100)
    # 显示静态（非交互式）表格
    st.table(df[('col %d' % i for i in range(10))][0:5])

    # 以格式化的JSON字符串显示对象或字符串
    st.json({
        'foo': 'bar',
        'baz': 'boz',
        'stuff': [
        'stuff 1',
        'stuff 2',
        'stuff 3',
        'stuff 5',
    ],})

def testChart():
    import matplotlib.pyplot as plt
    import altair as alt
    # 折线图
    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
    st.line_chart(chart_data)
    # 面积图
    st.area_chart(chart_data)
    # 条形图
    chart_data = pd.DataFrame(
        np.random.randn(50, 3),
        columns=["a", "b", "c"])

    st.bar_chart(chart_data)
    # 显示 matplotlib.pyplot图形
    arr = np.random.normal(1, 1, size=100)
    plt.hist(arr, bins=20)
    st.pyplot()

    # 使用Altair库绘制图表
    df = pd.DataFrame(
        np.random.randn(200, 3),
        columns=['a', 'b', 'c'])

    c = alt.Chart(df,height=300,width=500).mark_circle().encode(
        x='a', y='b', size='c', color='c')

    st.altair_chart(c)
    st.text("Altair图表例子：https://altair-viz.github.io/gallery/")

    # 使用Vega-Lite绘图
    df = pd.DataFrame(
        np.random.randn(200, 3),
        columns=['a', 'b', 'c'])

    st.vega_lite_chart(df, {
        'mark': 'circle',
        "width": 500, "height": 300,
        'encoding': {
            'x': {'field': 'a', 'type': 'quantitative'},
            'y': {'field': 'b', 'type': 'quantitative'},
            'size': {'field': 'c', 'type': 'quantitative'},
            'color': {'field': 'c', 'type': 'quantitative'},
        },
    })
    st.text("Vega-Lite图表例子：https://vega.github.io/vega-lite/examples/")
    # 交互式 Plotly 图表.
    import plotly.figure_factory as ff
    # Add histogram data
    x1 = np.random.randn(200) - 2
    x2 = np.random.randn(200)
    x3 = np.random.randn(200) + 2
    # Group data together
    hist_data = [x1, x2, x3]
    group_labels = ['Group 1', 'Group 2', 'Group 3']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(
            hist_data, group_labels, bin_size=[.1, .25, .5])
    # Plot!
    st.plotly_chart(fig)
    st.text("Plotly图表例子：https://plot.ly/python")
def testMedia():
    url='https://s1.ax1x.com/2020/03/20/86heKI.png'
    st.image(url)
    url="https://player.bilibili.com/player.html?aid=83262357&cid=142443560&page=1"
    st.video(url)

def testWidget():
    # 按钮
    if st.button('Say hello'):
        st.write('Why hello there')
    else:
        st.write('Goodbye')
    # 复选框
    agree = st.checkbox('I agree')

    if agree:
        st.write('Great!')
    dicts = {
        "a":"a1",
        "b":"b1"
    }
    selected_layers = [layer for layer_name, layer in dicts.items()if st.sidebar.checkbox(layer_name, True)]
    st.write(selected_layers)
    # 单选按钮
    genre = st.radio(
        "What's your favorite movie genre",
        ('Comedy', 'Drama', 'Documentary'))

    if genre == 'Comedy':
        st.write('You selected comedy.')
    else:
        st.write("You didn't select comedy.")
    # 下拉列表
    option = st.selectbox(
        'How would you like to be contacted?',
        ('Email', 'Home phone', 'Mobile phone'),index=2)
    st.write('You selected:', option)
    # 多项列表
    options = st.multiselect(
        'What are your favorite colors',
        ['Yellow', 'Red','Green', 'Yellow', 'Red', 'Blue'])
    st.write('You selected:', options)
    # 滑块
    # 返回数值
    age = st.slider('How old are you?', 0, 130, 25)
    st.write("I'm ", age, 'years old')  
    # 返回数值元组 
    values = st.slider(
        'Select a range of values',
        0.0, 100.0, (25.0, 75.0))
    st.write('Values:', values)
    # 文本输入
    title = st.text_input('Movie title', 'Life of Brian')
    st.write('The current movie title is', title)
    # 数值输入
    number = st.number_input('Insert a number')
    st.write('The current number is ', number)
    # 多行文本输入
    txt = st.text_area('Text to analyze', '''It was the best of times, it was the worst of times, it wasthe age of wisdom, it was the age of foolishness, it wasthe epoch of belief, it was the epoch of incredulity, (...)''')
    st.write("Sentiment:",txt)
    # st.write('Sentiment:', run_sentiment_analysis(txt))
    # 日期输入
    import datetime
    d = st.date_input(
        "When's your birthday",
        datetime.date(2019, 7, 6))
    st.write('Your birthday is:', d)   
    # 时间输入         
    t = st.time_input('Set an alarm for', datetime.time(8, 45))
    st.write('Alarm is set for', t)
    # 上传文件
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv","txt"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)

def testSide():
    """
    `st.sidebar.[ele_name]`在侧边框添加控件
    """
def testCode():
    # 这是完整代码
    import streamlit as st
    def get_user_name():
        return 'John'
    # with下的代码段将会显示出来
    with st.echo():
        # Everything inside this block will be both printed to the screen
        # and executed.

        def get_punctuation():
            return '!!!'

        greeting = "Hi there, "
        value = get_user_name()
        punctuation = get_punctuation()

        st.write(greeting, value, punctuation)

    # And now we're back to _not_ printing to the screen
    foo = 'bar'
    st.write('Done!')

def testStatus():
    import time
    # 进度条
    my_bar = st.progress(0)
    for percent_complete in range(5):
        time.sleep(0.1)
        my_bar.progress((percent_complete + 1)*20)
    # 代码段运行时显示的信息
    with st.spinner('Wait for it...'):
        time.sleep(2)
    st.success('Done!')
    selected1 = st.selectbox(
        "选择测试消息类型:",
        ("庆祝气球","错误","警告","提示","成功","异常")
    )
    if selected1 == "庆祝气球":
        st.balloons()
    elif selected1 == "错误":
        st.error('This is an error')
    elif selected1 == "警告":
        st.warning('This is a warning')
    elif selected1 == "提示":
            st.info('This is a purely informational message')
    elif selected1 == "成功":
        st.success('This is a success message!')
    elif selected1 == "异常":
        e = RuntimeError('This is an exception of type RuntimeError')
        st.exception(e)
def testPlh():
    """
    这里有占位符👇
    """
    my_placeholder = st.empty()
    vcb = st.checkbox("显示帮助")
    if vcb:
    # 可以使用text,write...类型填充:
        my_placeholder.help(pd.DataFrame)
    """
    ```python
    # 获取Steamlit的配置信息,返回指定选项的值
    # 使用streamlit config show命令查看详细配置项
    streamlit.get_option(key)
    # 修改配置, 目前只有client.caching, client.displayEnabled可在脚本中设置。
    streamlit.set_option(key, value)
    ```
    """
def testCache():
    """
    `streamlit.cache(func=None, persist=False, allow_output_mutation=False, show_spinner=True, suppress_st_warning=False, hash_funcs=None, ignore_hash=False)`
    """
def testMdat():
    # 在表格后追加数据
    df1 = pd.DataFrame(
    np.random.randn(10, 10),
    columns=('col %d' % i for i in range(10)))

    my_table = st.table(df1)
    df2 = pd.DataFrame(
    np.random.randn(5, 10),
    columns=('col %d' % i for i in range(10)))

    my_table.add_rows(df2)
    # Now the table shown in the Streamlit app containsthe data for
    # df1 followed by the data for df2.

    # 折线图后面添加数据
    # Assuming df1 and df2 from the example above still exist...
    my_chart = st.line_chart(df1)
    my_chart.add_rows(df2)
    # Now the chart shown in the Streamlit app contains the data for
    # # df1 followed by the data for df2.

def testAPI(show_code):
    import streamlit as st
    import inspect,textwrap
    itemDict = OrderedDict(
        [
            ("魔法命令",
            (testMgic,"魔法命令(Magic Commands)",
            """**Magic Commands 只能工作在Python3环境**  
            Steamlit会自动将每行的`变量`或`文本`自动使用`st.write()`方式显示到程序中,其中文本支持MarkDown。同时它会自动忽略文件、函数开头的说明文本.""")),
            ("文本",
            (testText,"文本(text)",
            """`st.title()`可以设置APP的标题,此外还有两个标题级别可以使用`st.header`和`st.subheader`.  
            其他文本函数:  
            `st.write`: 被称为瑞士军刀，可以自动显示多种数据类型，文本，变量，甚至图表等。`st.text()`: 纯文本  
            `st.markdown()`: Markdown(Github-flavored Markdow)  
            `st.code()`, `st.latex()`...""")),
            ("数据",
            (testDat,"数据(data)","格式化显示原始数据表格等信息")),
            ("图表",
            (testChart,"图表(chart)",
            """Streamlit支持Matplotlib、交互式图表[Vega Lite](https://vega.github.io/vega-lite/) (2D charts)和[deck.gl](https://github.com/uber/deck.gl) (maps and 3D charts)等图表库，同时Streamlit有一些“原生”绘图方式""")),
            ("多媒体",
            (testMedia,"多媒体(Media)",
            "嵌入图片、音频、视频文件")),
            ("控件",
            (testWidget,"交互控件(interactive widgets)",None)),
            ("边框",
            (testSide,"边框(Sidebar)","左边就是sidebar,里面嵌套了两个selectbox")),
            ("代码",
            (testCode,"代码(code)","`st.echo()`用于显示代码")),
            ("状态及进度",
            (testStatus,"进度条及状态提示信息",None)),
            ("占位符、帮助和选项",
            (testPlh,"占位符、帮助和选项(Placeholders, help, and options)",None)),
            ("追加数据",
            (testMdat,"追加数据(Mutate data)","Streamlit可以修改已有元素（chart、table、DataFrame）的数据")),
            ("优化性能",
            (testCache,"性能优化(Caching)",None))
        ]
    )
    testType = st.sidebar.selectbox("测试内容",list(itemDict.keys()))
    testFun = itemDict[testType][0]
    st.subheader(itemDict[testType][1])
    if itemDict[testType][2] != None:
        st.markdown(itemDict[testType][2])
    testFun()
    if show_code:
        st.write("## 代码")
        source_code, _ = inspect.getsourcelines(testFun)
        fsource = textwrap.dedent("".join(source_code[1:]))
        st.code(fsource)

from collections import OrderedDict

proj = OrderedDict(
    [
        ("目录",(content,"Steamlit 练习项目")),
        ("API测试",(testAPI,"API学习")),
        ("实例教程",(uber,"Uber pickups in NYC"))
    ]
)

def run():
    import streamlit as st
    projName = st.sidebar.selectbox("选择项目",list(proj.keys()), 0)
    projFUNC = proj[projName][0]
    st.write("# %s" % proj[projName][1])
    if projName == "目录":
        show_code =False
    else:
        show_code = st.sidebar.radio("是否显示代码",[True,False],index=0)
    projFUNC(show_code)


if __name__ == "__main__":
    run()
