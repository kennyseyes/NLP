#!/usr/bin/python
# -*- coding:utf-8 -*-
import codecs
import re
global N
global charlen #当前扫描字符占的字节数

class Dictionary:  #建立词典
    def __init__(self,file):
        self.n=N
        self.dictMap={}
        self.N=0  #number of words
        dictfile = open(file,'r')

        for eachLine in dictfile:
            l = eachLine.split("\n")[0]
            strlist = l.split("  ")  # 按n-gram将词存储

            s = ""
            num = 0
            for words in strlist:
                if words not in self.dictMap:
                    self.dictMap[words] = {}
                    self.N+=1

                if num >self.n-1:  # 不越界
                    for j in range(num-self.n+1,  num):
                        s = s + ' '+strlist[j]
                else:
                    lack = self.n - num  -1
                    for j in range(0, lack ):
                        s = s + " <start>"
                    for j in range(0, num):
                        s = s + " " + strlist[j]


                        # 统计词频
                if s not in self.dictMap[words]:  # 如果接下来的单词没有出现过
                    self.dictMap[words][s]=1
                else:
                    self.dictMap[words][s] += 1

                s = ""
                num += 1

        f = codecs.open("result.txt",'w')
        for key in self.dictMap:
            for innerkey in self.dictMap[key]:
                s=key+innerkey+str(self.dictMap[key][innerkey])+"\n"
                f.write(s)
        f.close()
        dictfile.close()

    def getKeyCount(self, key,w):  #某词出现次数 and 某词出现时，他前面出现的词的次数，用作n-gram统计概率
        word=' '+w
        if (self.dictMap.has_key(key)):
            sum_key=0
            for item in self.dictMap[key]:
                sum_key+=self.dictMap[key][item]
            if(self.dictMap[key].has_key(word)):
                sum_cond=self.dictMap[key][word]
                return (sum_key,sum_cond)
            else:
                return 0.5
        else:
            return 0.5  # 如果词典中没有，这个词的出现次数被定为 0.5

    def getPvalue(self, key,word):   #条件概率，n-gram
        if (self.dictMap.has_key(key)):
            return float(self.getKeyCount(key, word)[1]) / float(self.getKeyCount(key, word)[0])

        else:
            return 0.5




class MM:  #前向最大匹配分词
    def __init__(self, maxlen,testfile,dictionary,outfile):
        self.maxlen=maxlen  #最大词长度
        self.wordlist=[]  #分好的词
        self.dict=dictionary.dictMap #使用的语料库

        f=open(testfile,'r')
        o=open(outfile,'w')


        for l in f:
            line=l.split('\n')[0]
            line=line.split('\r')[0]
            start = 0
            if (len(line[start:]) > self.maxlen):#规定end位置，减少计算量
                end = self.maxlen
            else:
                end = len(line)

            word=line[start:end] #在start到end这段距离中找语料库中存在的词语
            while (not word ==""):
                search = re.search('[a-zA-Z0-9|.]+', line[start:])  # 找不可拆分的数字
                if search:
                    s = search.span()
                    if s[0]==0:
                        end=start+s[1]
                        word=line[start:end]
                        self.wordlist.append(word)
                       # print word
                        start=end
                        end= start+self.maxlen
                        word=line[start:end]
                    else:
                        # 过滤掉数字字母标点以免给分词造成影响
                        if (end >= start + s[0]):
                            end = s[0] + start
                            word = line[start:end]
                        if self.dict.has_key(word):  # 词典中有该词则将其存储在wordlist中
                            start = end
                            if (len(line[start:]) > self.maxlen):  # 规定end位置，减少计算量
                                end = start + self.maxlen
                            else:
                                end = len(line)

                            self.wordlist.append(word)
                           # print word
                            word = line[start:end]
                        else:  # 词典中没有该词则将最大长度-1后再匹配
                            end -= 3
                            word = line[start:end]
                            if (len(word) == 3):  # 找到最后只剩一个字发现没有匹配，则将其定为一个词
                                self.wordlist.append(word)
                                #print word
                                start += 3
                                if (len(line[start:]) > self.maxlen):  # 规定end位置，减少计算量
                                    end = start + self.maxlen
                                else:
                                    end = len(line)
                                word = line[start:end]
                else:
                    #过滤掉数字字母标点以免给分词造成影响
                    if(end>=start+self.maxlen):
                        end=self.maxlen+start
                        word = line[start:end]
                    if self.dict.has_key(word): #词典中有该词则将其存储在wordlist中
                        start=end
                        if (len(line[start:]) > self.maxlen):  # 规定end位置，减少计算量
                            end = start+self.maxlen
                        else:
                            end = len(line)

                        self.wordlist.append(word)
                        #print word
                        word=line[start:end]
                    else:  #词典中没有该词则将最大长度-1后再匹配
                        end-=3
                        word=line[start:end]
                        if (len(word)==3):   #找到最后只剩一个字发现没有匹配，则将其定为一个词
                            self.wordlist.append(word)
                            #print word
                            start += 3
                            if (len(line[start:]) > self.maxlen):  # 规定end位置，减少计算量
                                end = start+self.maxlen
                            else:
                                end = len(line)
                            word=line[start:end]

            for w in self.wordlist:
                 #print w
                o.write(w+"  ")

            o.write('\n')
            self.wordlist=[]
        f.close()
        o.close()




N=2
dict1 = Dictionary("pku_training.utf8")
maxlen=33 #设置最大长度11个汉字

print len("℃")

testfile="pku_test.utf8"
outfile="testresult.txt"
mm=MM(maxlen,testfile,dict1,outfile)
