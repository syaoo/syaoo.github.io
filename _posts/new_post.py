import os

header = '''
---
title: 
tag: ["tag1", "tag2"]
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover1.jpg
---
'''
context = '''
Abstract
<!--more-->
text
----
'''
ref = '''
**参考**
1. [title](url)
'''

title = input("post title is:")
fname = title+".md"
with open(fname,'w') as f:
	f.write(header)
	f.write(context)
	f.write(ref)
print("OK!")