### LaTex学习笔记
```tex
\documentclass[options]{style}
%style:article, book, report...
%导言区

\begin{document}
%正文区
\end{document}
```
#### 1.文档类
标准文档类的可选项
|功能|选项|说明|
|-|-|-|
|纸张大小|a4paper| |
|纸张方向|landscape|横向纸张 |
|分栏|onecolumn|单栏 |
||twocolumn|双栏|
|草稿设置|draft|草稿|
* frat可以加快编译速度
ctex宏包

|功能|选项|说明|
|-|-|-|
|排版|indent|标题后首行缩进
||noindent|首行不缩进
|宏包兼容|fancyhar|调用宏包并与之兼容
| |hyperref|调用宏包并与之兼容
#### 2.标题
分两部分：声明标题；显示标题
组成：名称、作者、时间...
a.在导言区声明

```tex
\title{}
\author{}
```

在正文区显示`\miketitle`
b.使用`titlepage`，以及wilson宏包
```tex
\begin(titlepage)

\end{titlepage}
```
#### 3.正文环境
**文本环境**
```tex
\begin{document}
\end{document}
```
**引用环境**
```tex
\begin{quote}
%首行无缩进
\end{quote}
```
```tex
\begin{quotation}
%首行有缩进
\end{quotation}
```
**诗词环境**
```tex
\begin{verse}
%以\\换行
\end{verse}
```
**摘要环境**
```tex
\begin{abstract}
\end{abstract}
```
**列表环境**</br>
`enumerate` 带有计数器</br>
`itemize` 不带计数器</br>
`description` 强制使用的可选参数作为关键字</br>
**定理环境**</br>
```tex
\newtheorem{theory}{name}
%这条命令放置在导言区，命令声明了定律环境，参数1是新定义的环境名称，环境2是显示在文档内地的输出标题名字。

%下面放在正文区
\begin{theory}[可选二标题]
%定理内容
\end{theory}
```
相关宏包`theorem`
```tex
\usepackage{theorem}
\theorembodyfont{font type} %set font in the theory environment.
\theoremheaderfont{font type} %set font type in the header of this environment.
\theorempreskipamount %vertical distance in the front of theorem using \setlength to set.
\theorempostskipamount %vertical distance after the theorem.
```
**抄录命令与环境**</br>
```tex
%%命令
\verb %用来表示文中的抄录
\verb<label>text<label> 两个label间的内容原样输出，label可以是任何相同的符号
\verb* 可以使输出的空格可见

%%环境
\begin{verbatim} %verbatim* 可以输出空格
\end{verbatim}
```
`fancyvrb`提供了verbatim的扩展

**代码环境**</br>
listings宏包，对应环境lstlisting
```tex
\usepackage{listings}
\begin{lstlisting}[language=python]
\end{lstlisting}
```
#### 4.盒子
水平盒子 无法进行段落划分、垂直盒子、不带边框的盒子、带边框的盒子</br>
```tex
%不带边框盒子
\mbox{text}
\makebox[width][position(C L R S)]{text}

%带边框盒子
\fbox{text}
\framebox[width][position]{text}

%垂直盒子，可以划分段落
% command style
\parbox{width(always like this: 0.84\textwidth)}{text}
% environment style
\begin{minipage}{width(always like this: 0.84\textwidth)}
text
\end{minipage}

\raisebox{distance}{etxt} %control the position of up & down + is up，- is down.
```
#### 5.字体族
字体族 font family :<br>
预定义字体族 

|字体族 |带参数命令| 声明命令|
|--|--|--|
|罗马|`\textrm{}`| `\rmfamily`|
|无衬线|`\textsf{}`|`\sffamily`
|打字机|`texttt{}`|`\ttfamily`
在ctex宏包中，正常字体->宋体，粗体->黑体，意大利体->楷体；且预置了宋体`\songti`，黑体`\heiti`，仿宋`\fangsong`，楷体`\kaiti`四种字体族。

基本字体设置-英文<br>
fontspec宏包设置字体（要放在ctex包后面）；对于英文，设置罗马字体族，无衬线字体族及打字机字体族
```tex
\setmainfont[options]{fontname}
\setsansfont[options]{fontname}
\setmonofont[options]{fontname}
% 设置好后fontspec会自动匹配相应字体；
% 也可以指定字体,如：
\setmainfont[
    BoldFont = heiti
    ItalicFont = heiti
    BoldItalicFont = heiti
]{heiti}
```
基本字体设置-中文
```tex
\setCJKmainfont[options]{fontname}
\setCJKsansfont[options]{fontname}
\setCJKmonofont[options]{fontname}
\setCJKfamilyfont{中文字体族}{字体名称} %自定义中文字体族
\CJKfamilyfont{中文字体族} %使用自定义中文字体族

% 重新定义新的字体族
\nwefontfamily<命令>[可选参数]{字体名}
\nweCJKfontfamily<命令>[可选参数]{字体名}
```
字体形状 font shape

字体系列 font series

#### 6.字号、水平间距与垂直间距
**英文字号**：字号命令表示的尺寸和行间距随文档类和其他因素影响，并不能准确表示字号大小。
```tex
\tiny           \scriptsize     \footnotesize   \small
\normalsize     \large          \Large          \LARGE
\huge           \HUGE   
```
**中文字号**：ctex中`\zihao{1}`一号，`\zihao{-1}`小一号；<br>
可重新定义命令，做到修改全局字体大小
```tex
\renewcommand\normalsize{\fontsize{18pt}{\baselineskip}\selectfont}

\linespread{factor} % 行间距命令,factor基本行距的倍数因子，默认文字大小1.2倍；
```
垂直间距
|command| founction|
|--|--|
|`\vskip{len}`|生成垂直方向间距为len的空白|
|`\vspace*{len}`|生成垂直方向间距为len的空白,存在问题不建议使用|
|`\vfill=\vspace{fill}`|垂直方向上分散均匀排列|
注意：len参数可以是 `\parskip`,`\itemsep`, `\smallskip`, `\medskip`, `\bigskip`..
latex常用单位
|单位|中文|大小|备注
|-|-|-|-
|pt|磅|1/72英寸||
|in|英寸|2.54cm||
|em||字号对应的长度|大小等于`\quad`,大写M的宽度|
|ex|||小写x的高度|
水平间距
|\quad|1em
|-|-|
|\qquad|2em
|\hspace{len}|生成水平方向大小为len的空白间距，行起始处不生效
|\hspace*{len}|生成水平方向大小为len的空白间距，行起始处生效，产生缩进效果
|\hfill=\hspace{fill}|水平方向上分散均匀排列

#### 7.文字强调
强调形式：斜体`\emph{}`，加粗`\textbf{}`，下划线`\underline{}`<br>
英文宏包： `\ulem`
```tex
\uline{} %下划线
\uuline{} %双下划线
\uwave{} %波浪线
\sout{} %划掉
```
中文宏包：\CJKfntef
```tex
\CJKunderline{} %
\CJKunderdot{} %
\CJKunderwave{} %
\CJKsout{} %
```
#### 7.整体文档架构
|长度变量|解释|
|-|-|
|`\paperwidth` `\paperheight`|纸张宽度、长度|
|`\textwidth` `\textheight`|版心宽度、长度，常用于设置图片大小|
|`\tomargin`|额外的上边缘|
|`\headheight`|页眉高度|
|`\headsep`|页眉与版心间距|
|`\marginparwidth`|边注宽带|
|`\marginparsep`|边注与版心间距|
|`\footskip`|页脚基线与正文最后一行的间距|
注：以上参数都可以使用`\setlength`设定 `\setlength\textwidth{7in}`.<br>
**geometry**宏包

#### 8.章节
|Latex章节层次
|-|
|\part : 可选的最高层次|
|\chapter : report book or ctexrep ctexbook 文档类的最高层次|
|\section : article or ctexart类的最高层次|
|\subsection : |
|\subsubsection : |
|\paragraph|
|\subparagraph|
章节层次自动编号，加*不自动编号；`\secnumdepth` 控制章节编号的层次；`\tocdepth` 控制章节编入目录的层次。

#### 9.段落
段落基本属性
|作用|命令|
|-|-
|首行固定缩进|\parindent|
|临时禁用缩进|\noindent|
|临时缩进|\indent|
|垂直间距，`\setlength`设置|\parskip
|两端均匀对齐|默认
|左对齐|\raggedright
|右对齐|\raggedleft
|居中对齐|\centering

|对齐|环境设置
|-|-
|左|`\begin{flushleft}\end{flushleft}`
|右|`\begin{flushright}\end{flushright}`
|居中|`\begin{center}\end{center}`
**宏包**<br>
lettrine 产生段落首字母下沉效果
`\lettrine {W}{ord} is power.` 
shapepar 排版特定形状的段落
`\heartpar{text}`
`\starpar{text}`
...<br>
**分栏**<br>

- 直接使用twocolumn定义双栏
  `\columnsep`栏间距，`\columnseprule`栏间竖线，`\columnwidth`栏宽，三者可以使用`\setlength`设置
- 使用multicol宏包定义多栏
```tex
\begin{multicols}{3}
%分三栏
\end{multicols}
```
#### 10 页码，页眉，页脚
**页码**<br>
```tex
\pagenumbering{roman} %使用罗马数字
%text
\newpage
\pagenumbering{arabic} %使用阿拉伯数字
% text
```
|名称|类型|
|-|-
|arabic|阿拉伯数字
|roman|小写罗马数字
|Roman|大写罗马数字
|alph|小写字母
|Alph|大写字母
**页眉页脚**<br>
Latex提供若干预定义页脚页眉风格
|页面风格||
|-|-
|empty|无页眉页脚
|plain|无页眉，页脚为居中页码
|headings|无页脚，页眉为章节名与页码
|myheadings|无页脚，页眉为页码

|||
|-|-
|\leftmark|应用到页眉页脚设置中，表示high-level(chapter,...)
|\rightmark|表示low-level(section,..)

|||
|-|-
|\pagestyle{页眉风格}|设定页面风格
|\thispagestyle{页面风格}|设定当前页面风格
fancyhdr宏包提供fancy页面风格，将页眉页脚分为六部分，两条线。

#### 11.公式
宏包 `amsmath`<br>
分类：行内公式 `$ 内容 $`；<br>
行间公式：不带标号`$$内容$$`, `\[内容\]`, `\begin{displaymath}...\end{displaymath}`<br>
带标号: `\begin{equation}...\end{equation}`<br>
公式内中文`\text{中文}`

分数形式：`\frac{fenzi}{fenmu}`, `\dfrac{}{}`适用于行间公式中使用。

上下标：`mathtools`宏包实现符合前面的上下标。
前置脚标：`\prescript{前上}{前下}`, 四周角标 `\sideset{_1^2}{_3^4}`

化学公式<br>
`mhchem`宏包 `\ce{H_2O + Al -> Al_2O_3}`

`amsmath`中提供的命令：`\overline{neirong}`, `\underline{neirong}`, `\overbrace{nei}^{shanghuakuohao}`, `\underbrace{nei}_{shanghuakuohao}`
加箭头：`\over(under)(right)(left)arrow{neirong}`

`\sqrt[次数]{被开方数}` 