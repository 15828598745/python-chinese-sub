import re
import os
# 是否在<template>标签内
templateState = 0
notesState = 0
scriptState = 0
# 匹配html内的中文
reg_1 = '([\u4E00-\u9FA5]+\w+)(?=\<\/)'
reg_2 = '(?<=\s)([\u4E00-\u9FA5]+\w+)'
reg_3 = '\w+\=\"[\u4E00-\u9FA5]+\w+\"'
# 匹配script内的中文
reg_4 = '((\"|\'|`)[\u4E00-\u9FA5]+\w+(\"|\'|`))'

zhArr = []

def getCode(sList,regNum):
  for zh in sList:
    if regNum == 3:
      zh = re.findall("[\u4E00-\u9FA5]+\w",zh)
    if zh in zhArr:
      return "code_" + str(zhArr.index(zh))
    else:
      zhArr.append(zh)
      return "code_" + str(len(zhArr) - 1)
  return "code"

def replaceStr(regNum,sList,line):
  code = getCode(sList,regNum)
  if regNum == 1:
    str1 = re.sub(reg_1,"{{$t(\""+code+"\")}}",line)
    if str1 :
      return str1  
  if regNum == 2:
    str1 = re.sub(reg_2,"{{$t(\""+code+"\")}}",line)
    if str1 :
      return str1
  if regNum == 3:
    attr = re.findall("(\w+)(?=\=)",sList[0])
    str1 = re.sub(reg_3,":"+attr[0]+"=\"$t(\'"+code+"\')\"",line)
    if str1 : 
      return str1
  if regNum == 4:
    str1 = re.sub(reg_4,"this.$t(\""+code+"\")",line)
    if str1 :
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

def getAllVueFile(dir_path):
  a = []   
  for root, dirs, files in os.walk(dir_path):  
    for file in files:  
      if os.path.splitext(file)[1] == '.vue':  
        a.append(os.path.join(root, file))
  return a

def handel(old,new):
  global templateState
  global scriptState
  f1 = open(old,'r')
  allLines = f1.readlines()
  f2 = open(new, "w")
  for line in allLines :
    if re.findall('<template>',line):
      templateState += 1
      f2.write(line)
      continue
    if re.findall('</template>',line):
      templateState -= 1
      f2.write(line)
      continue
    # html
    if templateState > 0: 
      isIn = isInNotes(line)
      if notesState > 0 or isIn == True:
        f2.write(line)
        continue
      sList = re.findall(reg_1,line)
      if sList :
        f2.write(replaceStr(1,sList,line) )
        continue
      sList = re.findall(reg_2,line)
      if sList : 
        f2.write(replaceStr(2,sList,line))
        continue
      sList = re.findall(reg_3,line)
      if sList : 
        f2.write(replaceStr(3,sList,line))
        continue
    # javascript
    if re.findall('<script',line):
      scriptState += 1
      f2.write(line)
      continue
    if re.findall('\<\/script>',line):
      scriptState -= 1
      f2.write(line)
      continue
    
    if scriptState > 0:
      isIn = isInNotes(line)
      if notesState > 0 or isIn == True:
        f2.write(line)
        continue
      sList = re.findall(reg_4,line)
      if sList : 
        f2.write(replaceStr(4,sList,line))
        continue
    # style 不用翻译
    f2.write(line)

def run(enter,out):
  pathList = getAllVueFile(enter)
  for path in pathList:
    reg = "(\/\w+)"
    path1 = re.findall(reg,enter)
    print(path1)
    # path1 = os.path.join(out,path1[0])
    # # 无文件夹时创建
    # catalog = path1[0:path1.rfind("/")]
    # if not os.path.isdir(catalog):  
    #   os.makedirs(catalog)
    # if not os.path.isfile(path1):  # 无文件时创建
    #   fd = open(path1, mode="w", encoding="utf-8")
    #   fd.close()
    # handel(path,path1)

run("/home/lh/work/liahng/sav/admin-client/src/views","./new")
  


  
