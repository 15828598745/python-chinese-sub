import re
import os
import shutil
# 是否在<template>标签内
templateState = 0
notesState = 0
scriptState = 0
# 匹配html内的中文
reg_1 = '([\u4E00-\u9FA5]+\s?\w+)(?=\<\/)'
reg_2 = '(?<=\s)([\u4E00-\u9FA5]+\w+)'
reg_3 = '(\w+-?)+="[\u4E00-\u9FA5]+\w+:?"'
# 匹配script内的中文
reg_4 = '(\"|\'|`)[\u4E00-\u9FA5]+\w+(\?|\？|\！|\!)?(\"|\'|`)'

zhArr = []

def getCode(sList,regNum):
  a = []
  for strZh in sList:
    if regNum == 3:
      strZh = re.finditer("[\u4E00-\u9FA5]+\w:?",strZh)
      for match in strZh:
        strZh = match.group()
    if strZh in zhArr: 
      a.append("code_" + str(zhArr.index(strZh)))
    else:
      zhArr.append(strZh)
      a.append("code_" + str(len(zhArr) - 1))
  return a

def replaceStr(regNum,sList,line):
  code = getCode(sList,regNum)
  if regNum == 1:
    str1 = line
    for val in code:
      str1 = re.sub(reg_1,"{{$t(\""+val+"\")}}",str1,1)
    return str1  
  if regNum == 2:
    str1 = line
    for val in code:
      str1 = re.sub(reg_2,"{{$t(\""+val+"\")}}",str1,1)
    return str1
  if regNum == 3:
    str1 = line
    for i in range(len(sList)):
      attr = re.finditer("(\w+-?)+(?=\=)",sList[i])
      for match in attr:
        attr = match.group()
      str1 = re.sub(reg_3,":"+attr+"=\"$t(\'"+code[i]+"\')\"",str1,1)
    return str1
  if regNum == 4:
    str1 = line
    for val in code:
      str1 = re.sub(reg_4,"this.$t(\""+val+"\")",str1,1)
    return str1
  return line

def isInNotes(line):
  isIn = False
  global notesState
  if templateState > 0:
    ret = re.findall("\<\!\-\-",line)
    if ret:
      notesState += 1
      isIn = True
    ret = re.findall("\-\-\>",line)
    if ret:
      notesState -= 1
      isIn = True
  else :
    ret = re.findall("\/\/",line)
    if ret :
      isIn = True
      return isIn
    ret = re.findall("\/\*",line)
    if ret : 
      notesState += 1
      isIn = True
    ret = re.findall("\*\/",line)
    if ret :
      notesState -= 1
      isIn = True
  return isIn

def finditer(reg,line):
  a = []
  str1 = re.finditer(reg,line)
  for match in str1:
    a.append(match.group())
  if len(a) > 0:
    return a
  else :
    return False

def handel(old,new):
  global templateState
  global scriptState
  global notesState
  templateState = 0
  scriptState = 0
  notesState = 0
  f1 = open(old,'r')
  allLines = f1.readlines()
  f2 = open(new, "w")
  for line in allLines :
    if re.findall("<template",line):
      templateState += 1
      f2.write(line)
      continue
    if re.findall("</template",line):
      templateState -= 1
      f2.write(line)
      continue
    # html
    if templateState > 0: 
      isIn = isInNotes(line)
      if notesState > 0 or isIn == True:
        f2.write(line)
        continue
      sList = finditer(reg_1,line)
      if sList :
        f2.write(replaceStr(1,sList,line) )
        continue
      sList = finditer(reg_2,line)
      if sList : 
        f2.write(replaceStr(2,sList,line))
        continue
      sList = finditer(reg_3,line)
      if sList : 
        f2.write(replaceStr(3,sList,line))
        continue
    # javascript
    if re.findall("<script",line):
      scriptState += 1
      f2.write(line)
      continue
    if re.findall('</script',line):
      scriptState -= 1
      f2.write(line)
      continue
    
    if scriptState > 0:
      isIn = isInNotes(line)
      if notesState > 0 or isIn == True:
        f2.write(line)
        continue
      sList = finditer(reg_4,line)
      if sList : 
        f2.write(replaceStr(4,sList,line))
        continue
    # style 不用翻译
    f2.write(line)
  f1.close()
  f2.close()

def getAllVueFile(dir_path):
  a = []   
  for root, dirs, files in os.walk(dir_path):  
    for file in files:  
      if os.path.splitext(file)[1] == '.vue':  
        a.append(os.path.join(root, file))
  return a

def delOutAllFile(filepath):
  del_list = os.listdir(filepath)
  for f in del_list:
      file_path = os.path.join(filepath, f)
      if os.path.isfile(file_path):
        os.remove(file_path)
      elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
def outCodeConf(path):
  file = os.path.join(path,"zh.js")
  fd = any
  if not os.path.isfile(file):  
    fd = open(file, mode="w", encoding="utf-8")
  fd = open(file, mode="w", encoding="utf-8")
  fd.write(
    "import zhLocale from 'element-ui/lib/locale/lang/zh-CN'\r\n"+
    "export const zh = {\r\n"
  )
  for i in range(len(zhArr)):
    fd.write(
     "\"code_" + str(i) + "\": \"" + zhArr[i] + "\",\r\n"
    )
  fd.write("}")
  fd.close()

def run(enter,out):
  pathList = getAllVueFile(enter)
  for path in pathList:
    path1 = path.split(enter)
    # 把/符号删掉 不然拼接不上
    path1 = re.sub("^\/","",path1[1])
    print("now run file:",path1)
    path1 = os.path.join(out,path1)
    # 无文件夹时创建
    catalog = path1[0:path1.rfind("/")]
    if not os.path.isdir(catalog):  
      os.makedirs(catalog)
    # 无文件时创建
    if not os.path.isfile(path1):  
      fd = open(path1, mode="w", encoding="utf-8")
      fd.close()
    handel(path,path1)
  outCodeConf(out)

# handel("./old/index.vue","./new/index.vue")
# run("/home/lh/work/liahng/sav/admin-client/src/views","./new")
run("./old","./new")
