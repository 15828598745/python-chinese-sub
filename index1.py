
import re
str1 = 'this.v = "ip132测试代码123?",this.c = "测试代码"'
str3 = 'label="VIP视频收益123(元)"'
# '((\w+-?)+=".*?")[\u4E00-\u9FA5]+'

str2 = re.finditer('\w*[\u4E00-\u9FA5]+\w+(\?|\？|\！|\!)?',str1)
for match in str2: 
  print (match.group())
