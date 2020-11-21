
import re
str1 = '<el-table-column t-t-t-prop="dateTime" label="ID" align="center"></el-table-column>'


str2 = re.finditer('(\w+-?)+(?=\=)',str1)
for match in str2: 

  print (match.group())
