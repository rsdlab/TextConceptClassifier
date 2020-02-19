#!/usr/bin/env python
# -*- coding:utf-8 -*-

#from __future__ import print_function
import numpy as np
import keras
import glob
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split ### 追加
import wakati
import ast
#262
max_words = 270
batch_size = 32
epochs = 22

print('Loading data...')
 
dic={} # 辞書初期化
count = 0 # 辞書登録用カウンタ
folder = ["0","1","2","3","4","5","6","7","8"]
x, y = [], []
print ("text")

for index, name in enumerate(folder):
    dir = "/home/rsdlab/workspace/TextConceptClassifier/" +name
    files = glob.glob(dir + "/*.wakati")
    for i, file in enumerate(files):
        with open(file, "r", encoding='utf-8') as f:
            text=f.read()
            text=text.strip()
            text=text.split(" ")
            print ("textdata",text)
            print ("textdatatype",type(text))
            result = [] # 単語の数字化結果を入れるリスト
            for word in text:
                word = word.strip()
                #print ("worddata",word)
                if word == "": continue
                if not word in dic: # 未登録の場合
                    dic[word] = count # count の数字で辞書に登録
                    num = count
                    count +=1
                    print(num,word) # 数字と単語を表示
                else:
                    num=dic[word] # 数字を辞書で調べる
                result.append(num) # リストに数字を追加
            x.append(result) # リストを配列 ｘ に追加
            y.append(index) # フォルダー名を配列 y に追加

print ("datadic",dic)
open("wordlist.txt", "w").write(str(dic))

#f2 = open("wordlist.txt", "r").read()
#print (f2)
#print ("f2datatype",type(f2))
#f3 = ast.literal_eval(f2)
#print ("f3datatype",type(f3))

x_train = x
#,
x_test = x
#,
y_train = y
#,
y_test = y
#train_test_split(x, y, test_size=0.8, random_state = 111)
#print(len(x_train), 'train sequences')
#print(len(x_test), 'test sequences')
#print(type(x[0]))
#print(x[0])
print(type(x_test))
print(x_test)
print(type(x_train))
print(x_train)
 
num_classes = np.max(y_train) + 1
print(num_classes, 'classes')
 
print('Vectorizing sequence data...')
tokenizer = Tokenizer(num_words=max_words)
x_train = tokenizer.sequences_to_matrix(x_train, mode='binary')
x_test = tokenizer.sequences_to_matrix(x_test, mode='binary')
print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)
print(x_test)
 
print('Convert class vector to binary class matrix '
'(for use with categorical_crossentropy)')
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
print('y_train shape:', y_train.shape)
print('y_test shape:', y_test.shape)
 
print('Building model...')
model = Sequential()
#model.add(Dense(5290, activation='relu', input_dim=max_words))
#model.add(Dropout(0.5))
#model.add(Dense(5290, activation='relu'))
#model.add(Dropout(0.5))
#model.add(Dense(num_classes, activation='softmax'))
model.add(Dense(512, input_shape=(max_words,)))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))
 
model.compile(loss='categorical_crossentropy',
optimizer='adam',
metrics=['accuracy'])

history = model.fit(x_train, y_train,
batch_size=batch_size,
epochs=epochs,
verbose=1,
#validation_split=0.1
)

score = model.evaluate(x_test, y_test,batch_size=batch_size, verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])
 
### Plot accuracy
#import matplotlib.pyplot as plt
#acc = history.history["acc"]
#val_acc = history.history["val_acc"]
#epochs = range(1, len(acc) + 1)
# 
#plt.plot(epochs, acc, "bo", label = "Training acc" )
#plt.plot(epochs, val_acc, "b", label = "Validation acc")
#plt.title("Training and Validation accuracy")
#plt.legend()
#plt.savefig("acc.png")
#plt.close()
 
### plot Confusion Matrix
#import pandas as pd
#import seaborn as sn
#from sklearn.metrics import confusion_matrix
 
#def print_cmx(y_true, y_pred):
#    labels = sorted(list(set(y_true)))
#    cmx_data = confusion_matrix(y_true, y_pred, labels=labels)
#
#    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)
#
#    plt.figure(figsize = (10,7))
#    sn.heatmap(df_cmx, annot=True, fmt="d") ### ヒートマップの表示仕様
#    plt.title("Confusion Matrix")
#    plt.xlabel("predict_classes")
#    plt.ylabel("true_classes")
#    plt.savefig("c_matrix.png")
#    plt.close()

# モデルの構造を保存する
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

# モデルの重みを保存する
model.save_weights("model.h5")

#print(type(x_test[1:10,]))
#print(len(x_test[1:10,]))
#print(type(x_test[1:10][0]))
#print(x_test[1:10][0])
predict_classes = model.predict_classes(x_test, batch_size=batch_size) ### 予測したラベルを取得
print(type(predict_classes))
print(predict_classes)
#true_classes = np.argmax(y_test,1) ### 実際のラベルを取得
#print(confusion_matrix(true_classes, predict_classes))
#print_cmx(true_classes, predict_classes)

