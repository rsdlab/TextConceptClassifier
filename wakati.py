#!/usr/bin/env python
# -*- coding:utf-8 -*-
import MeCab
import os, glob
 
# 分かち書きし、日本語から名詞のみ抽出する
def ja_tokenize(text):
    res=[]
    lines=text.split("\n")
    tag = MeCab.Tagger ("-Ochasen")
    tag.parse('')
    for line in lines:
        print(type(line))
        malist=tag.parseToNode(line)
        while malist:
            resorg = malist.feature.split(',')[6]
            ps=malist.feature.split(",")[0]
            if ps == "名詞":
                if resorg != "*":
                    res.append(resorg)
            if ps == "動詞":
                res.append(resorg)
            if ps == "形容詞":
                res.append(resorg)
            if ps == "副詞":
                res.append(resorg)
            if ps == "助詞":
                res.append(resorg)
            if ps == "接続詞":
                res.append(resorg)
            if ps == "助動詞":
                res.append(resorg)
            if ps == "連体詞":
                res.append(resorg)
            if ps == "感動詞":
                res.append(resorg)
            res.append("\n")
            malist = malist.next
    return res

dir ='/home/rsdlab/workspace/TextConceptClassifier'

for path in glob.glob(dir + "/*/*.txt", recursive=True):
    # LICENSE.txtは以下の処理をスキップ
    if path.find("CMakeLists")>0:continue          
    print(path)
    path_wakati=path + ".wakati"
    # 既に "wakati"ファイルがあれば以下の処理をスキップ
    if os.path.exists(path_wakati):continue        
    text=open(path,"r", encoding='utf-8').read() 
    words=ja_tokenize(text)
    print(type(words))
    wt=" ".join(words)
    open(path_wakati, "w", encoding="utf-8").write(wt)
