#!/usr/bin/python
# -*- coding:utf-8 -*-
import codecs
import re

class Dictionary:  #建立词典
    def __init__(self,file):
        self.dictMap={}
        self.N=0  #词的数量，不包括重复的
        dictfile = open(file,'r')

        for eachLine in dictfile:
            l = eachLine.split("\n")[0]
            strlist = l.split("  ")  # 按n-gram将词存储

            num = 0  #总词数，包括重复的
            for words in strlist:
                if words not in self.dictMap:
                    self.dictMap[words] = 1
                    self.N+=1

                num += 1

        dictfile.close()



class MM:  #前向最大匹配分词
    def __init__(self, maxlen,testfile,dictionary,outfile):
        self.seg_list={}  #分出单词的字典
        self.maxlen=maxlen  #最大词长度
        self.wordlist=[]  #分好的词
        self.dict=dictionary.dictMap #使用的语料库
        self.word_correctly_seg=0  #正确分出的词

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
                search = re.search('β|×|·|[.a-zA-Z0-9]+', line[start:])  # 找不可拆分的数字
                if search:
                    s = search.span()
                    if s[0]==0:
                        end=start+s[1]
                        word=line[start:end]
                        self.wordlist.append(word)
                        if(self.seg_list.has_key(word)): #增加词的出现次数
                            self.seg_list[word]+=1
                        else:
                            self.seg_list[word]=1 #创建键值
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
                            if (self.seg_list.has_key(word)):  # 增加词的出现次数
                                self.seg_list[word] += 1
                            else:
                                self.seg_list[word] = 1  # 创建键值
                           # print word
                            word = line[start:end]
                        else:  # 词典中没有该词则将最大长度-1后再匹配
                            end -= 3
                            word = line[start:end]
                            if (len(word) == 3):  # 找到最后只剩一个字发现没有匹配，则将其定为一个词
                                self.wordlist.append(word)
                                if (self.seg_list.has_key(word)):  # 增加词的出现次数
                                    self.seg_list[word] += 1
                                else:
                                    self.seg_list[word] = 1  # 创建键值
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
                        if (self.seg_list.has_key(word)):  # 增加词的出现次数
                            self.seg_list[word] += 1
                        else:
                            self.seg_list[word] = 1  # 创建键值
                        #print word
                        word=line[start:end]
                    else:  #词典中没有该词则将最大长度-1后再匹配
                        end-=3
                        word=line[start:end]
                        if (len(word)==3):   #找到最后只剩一个字发现没有匹配，则将其定为一个词
                            self.wordlist.append(word)
                            if (self.seg_list.has_key(word)):  # 增加词的出现次数
                                self.seg_list[word] += 1
                            else:
                                self.seg_list[word] = 1  # 创建键值
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
        for word_seg in self.seg_list:
            if(self.dict.has_key(word_seg)):
                self.word_correctly_seg+=1

    def precision(self):
        return float(self.word_correctly_seg) / float(len(self.seg_list))

    def recall(self):
        return float(self.word_correctly_seg) / float(len(self.dict))




print "正在导入词典..."
dict1 = Dictionary("pku_training.utf8")
maxlen=33 #设置最大长度11个汉字

testfile="pku_test.utf8"
outfile="seg_result.txt"

print "正在进行分词.."
mm=MM(maxlen,testfile,dict1,outfile)
print "分词完成！"
p= mm.precision()
r=mm.recall()
f=2*p*r/(p+r)

print ("precision:%f"%(p))
print ("recall:%f"%(r))
print ("F measure:%f"%(f))
