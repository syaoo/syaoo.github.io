---
title: 数据类型
date: 2022-05-08 23:54
tag: ['python']
mathjax: false
mathjax_autoNumber: true
# Mermaid
mermaid: false
# Chart
chart: false
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---

## 根据网易云音乐ID获取歌曲详细信息

![](/assets/post_pic/163music_browser_f12.png)

[greats3an/pyncm: 网易云音乐 Python API / 下载工具](https://github.com/greats3an/pyncm)
[Binaryify/NeteaseCloudMusicApi: 网易云音乐 Node.js API service](https://github.com/Binaryify/NeteaseCloudMusicApi)






音乐下载API：浏览器开发者工具-网络-media中可以找到，但是实现自动化下载可能不容易。

### 文件元数据

[[原创]MP3文件的数据结构以及为mp3内嵌歌词的代码 — 编程爱好者社区](http://bbs.pfan.cn/post-372622.html)


As well as identifying the file format, file headers may contain metadata about the file and its contents. For example, most image files store information about image format, size, resolution and color space, and optionally authoring information such as who made the image, when and where it was made, what camera model and photographic settings were used (Exif), and so on. Such metadata may be used by software reading or interpreting the file during the loading process and afterwards.
[File format - Wikipedia](https://en.wikipedia.org/wiki/File_format)



# Python异常处理

语法错误和异常。

基于Python 3

使用 else 子句比向 try 子句添加额外的代码要好，可以避免意外捕获非 try ... except 语句保护的代码触发的异常。

## try...except

## else语句

## finally语句

## 常见标准异常


某些情况下捕获异常后，完成所需操作如日志记录等操作，可以使用raise重新抛出捕获的异常。
```python
try:
   # 需要检测异常的代码
except Exception as e:
   # 处理异常信息
   ...

   # 传播异常
   raise
```
异常链
```python
import sys
def func01():
    try:
        raise ValueError("N/A is Not Nub.")
    except ValueError as e:
        print("Exception args is:",e.args)

def func02():
    try:
        raise ValueError("N/A is Not Nub.")
    except ValueError as e:
        raise RuntimeError("Somethin Error in Runtime...")

def func03():
    try:
        raise ValueError("N/A is Not Nub.")
    except ValueError as e:
        raise RuntimeError("Somethin Error in Runtime...") from ValueError

def func04():
    try:
        raise ValueError("N/A is Not Nub.")
    except ValueError as e:
        raise RuntimeError("Somethin Error in Runtime...") from None
if __name__=="__main__":
    a=sys.argv[1]
    if (a== '1'):
        func01()
    elif a=='2':
        func02()
    elif a=='3':
        func03()
    elif a=='4':
        func04()
```

MRO（Method Resolution Order）：方法解析顺序。

1. [Python try except else（异常处理）用法详解](http://c.biancheng.net/view/2315.html)
2. [8. 错误和异常 — Python 3.10.4 文档](https://docs.python.org/zh-cn/3/tutorial/errors.html)
3. [第十四章：测试、调试和异常 — python3-cookbook 3.0.0 文档](https://python3-cookbook.readthedocs.io/zh_CN/latest/chapters/p14_test_debug_and_exceptions.html)
4. [Python3 错误和异常 | 菜鸟教程](https://www.runoob.com/python3/python3-errors-execptions.html)
5. [Python 异常处理 | 菜鸟教程](https://www.runoob.com/python/python-exceptions.html)

---

**参考**
1. [title](url)