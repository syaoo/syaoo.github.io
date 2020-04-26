XML（可扩展标记语言，EXtensible Markup Language）是一种固有的分层数据格式，用于数据传输与存储。XML文档就像一棵树，必须包含一个（且仅一个）根元素，它是其他元素的父元素，然后不断扩展开枝散叶。XML 元素指的是从（且包括）开始标签直到（且包括）结束标签的部分， 每个元素必须包含一个标签，也可以包含属性、文本以及其他元素。下面是一个XML元素，`tag`是元素标签，`'attris'="属性"`是元素的属性，`text`是元素包含的文本。
 ```xml
 <tag 'attris'="属性"> text </tag>
 ```
[`xml.etree.ElementTree`](https://docs.python.org/zh-cn/3/library/xml.etree.elementtree.html) 模块实现了一个简单高效的API，用于解析和创建XML数据。ElementTree有两个类，分别用于表示XML树及其元素，ElementTree通常用于整个文档的操作，而Element用于对元素节点的处理。



---

参考：  
[XML 教程 | 菜鸟教程]( https://www.runoob.com/xml/xml-tutorial.html)  
[xml.etree.ElementTree --- ElementTree XML API](https://docs.python.org/zh-cn/3/library/xml.etree.elementtree.html)