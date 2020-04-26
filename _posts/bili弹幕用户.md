---
title: YAML
tag: ["YAML", "PyYAML"]
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover0.jpg
---
从弹幕列表看到用户加密后id（十六进制）
import binascii
for i in range(1,1000000000):
    if binascii.crc32(str(i).encode("utf-8")) == 0xc2dfa687: #c2dfa687 -> 326480710 # 6d8daf80
        print(i)
http://comment.bilibili.com/cid.xml
http://articles.kevinz.cn/2017/12/20/sender/