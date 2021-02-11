#!/bin/bash
# 此程序用於自動創建一個文章框架，
# 包含文章的yaml頭信息，摘要，正文以及參考文獻四部分。
# v1.0
# 下一步计划加入对background_image的选择、及其他Yaml头信息的丰富
# v1.01 
# 更新：随机background_image，更变yaml头字符串组织方式；
# v1.02
# 添加 chart、mermaid等设置
#
# TODO：增加自定义选项

# ************************************
# 寫入函數
front(){
    # 寫入YAML頭信息
    # 第一個參數作爲文件名
    # 另、可加一個參數作爲文章標題
    bs="\040\040" #Octal ASCII code space
    bs2="\040\040\040\040"
    pics=4 # number of pictures
    time=`date "+%Y-%m-%d %H:%M"`
    sec=`date +%s`
    num=`expr $sec % $pics` 
    echo "---" >> $1
    if test -e $2
    then
        title=$1
    else
        title=$2
    fi
    context="title: $title\n\
date: ${time}\n\
tag: ['tag1','tag2']\n\
mathjax: false\n\
mathjax_autoNumber: true\n\
# Mermaid\n\
mermaid: false\n\
# Chart\n\
chart: false\n\
article_header:\n\
${bs}type: overlay\n\
${bs}theme: dark\n\
${bs}background_color: '#203028'\n\
${bs}background_image:\n\
${bs2}gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'\n\
${bs2}src: /assets/images/cover${num}.jpg"
    echo -e $context >> $1
    echo "---" >> $1
}

abstract(){
    echo -e "\nabstract\n" >> $1
    echo "<!--more-->" >> $1
}

context(){
    echo -e "\ncontext\n" >> $1
    echo -e "\n---\n" >> $1
}

refer(){
    echo "**参考**" >> $1
    echo "1. [title](url)" >> $1
}

# ************************************
# Main
if test $1
# $1爲文件名，如果沒有指定，則讓用戶輸入
then
    fname=$1
    echo "file name is $fname"
else
    # echo -n "PLZ input file name:"
    # read fname
    read -p "PLZ input file name:" fname
    echo "you input file name is $fname"
fi

#  檢查文件名中是否包含markdown擴展名`.md`.
len_fn=${#fname}
bg=$[len_fn-3]
md=${fname:bg:len_fn}
if [ "$md" != '.md' ]
then
    fname="${fname}.md"
    echo $fname
fi

# 檢查文件是否存在
if test -e $fname
then
    typeset -u yon # 設置變量you值爲大寫，-l爲小寫
    read -p "File $fname already exists, overwrite or not?[Y/N(default)]" yon
    if [[ $yon = 'Y' ]]
    # 使用`[[ ]]`避免当yon为空时出现`=: unary operator expected`错误
    then
        rm $fname
    else
        echo "abort!!!"
        exit 1
    fi
fi

title=${fname/.md/}
typeset -u yon # 設置變量you值爲大寫，-l爲小寫
read -p "Use <<$title>> as article title?[Y/N(default)]" yon
# if ! [ \( $yon = 'N' \) -o \( -z $yon \) ]
if [[ $yon != 'Y' ]]
then
    read -p "Input article title: " title
fi
echo "This article title is <<$title>>."
# 開始寫入文件
touch $fname
front $fname $title
abstract $fname
context $fname
refer $fname
echo "done!"
# echo "Open file with SublimeText"
# subl $fname