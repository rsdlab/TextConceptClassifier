#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file TextConceptClassifier.py
 @brief TextConceptClassifier
 @date $Date$


"""
import sys
import time

sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import SpeechManage_idl

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
import Manage, Manage__POA

import MeCab
import os

import numpy as np
import keras
import glob
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy

import chardet

import ast

import pickle

max_words = 270
batch_size = 32

# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
textconceptclassifier_spec = ["implementation_id", "TextConceptClassifier",
		 "type_name",         "TextConceptClassifier",
		 "description",       "TextConceptClassifier",
		 "version",           "1.0.0",
		 "vendor",            "hiroyasu",
		 "category",          "Category",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class TextConceptClassifier
# @brief TextConceptClassifier
#
#
class TextConceptClassifier(OpenRTM_aist.DataFlowComponentBase):

	##
	# @brief constructor
	# @param manager Maneger Object
	#
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_textIn = RTC.TimedStringSeq(RTC.Time(0,0),"")
		"""
		"""
		self._textInIn = OpenRTM_aist.InPort("textIn", self._d_textIn)

		"""
		"""
		self._speechmanagePort = OpenRTM_aist.CorbaPort("speechmanage")



		"""
		"""
		self._SpeechManageRequire = OpenRTM_aist.CorbaConsumer(interfaceType=Manage.SpeechManage)
                self.loaded_model = None

                self.dic = None

		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">

		# </rtc-template>



	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry()
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onInitialize(self):
		# Bind variables and configuration variable

		# Set InPort buffers
		self.addInPort("textIn",self._textInIn)

		# Set OutPort buffers

		# Set service provider to Ports

		# Set service consumers to Ports
		self._speechmanagePort.registerConsumer("SpeechManage", "Manage::SpeechManage", self._SpeechManageRequire)

		# Set CORBA Service Ports
		self.addPort(self._speechmanagePort)

		return RTC.RTC_OK

	###
	##
	## The finalize action (on ALIVE->END transition)
	## formaer rtc_exiting_entry()
	##
	## @return RTC::ReturnCode_t
	#
	##
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK

	###
	##
	## The startup action when ExecutionContext startup
	## former rtc_starting_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The shutdown action when ExecutionContext stop
	## former rtc_stopping_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK

	##
	#
	# The activated action (Active state entry action)
	# former rtc_active_entry()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onActivated(self, ec_id):
                # モデルの構造を読む
                json_file = open('model.json', 'r')
                loaded_model_json = json_file.read()
                json_file.close()
                self.loaded_model = model_from_json(loaded_model_json)

                self.loaded_model.compile(loss='categorical_crossentropy',
                                     optimizer='adam',
                                     metrics=['accuracy'])

                # 重みを適用する
                self.loaded_model.load_weights("model.h5")

                f = open("wordlist.txt", "r").read()
                
                self.dic = ast.literal_eval(f)
	
		return RTC.RTC_OK

	##
	#
	# The deactivated action (Active state exit action)
	# former rtc_active_exit()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onDeactivated(self, ec_id):
	
		return RTC.RTC_OK

	##
	#
	# The execution action that is invoked periodically
	# former rtc_active_do()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onExecute(self, ec_id):
                while self._textInIn.isNew():
                        ut = time.time()
                        print (int(ut*100000))
                        stockdata =[]
                        indata = self._textInIn.read()
                        #indata = "右側にあるドリンクを取って"
                        print (indata)
                        for pointdata in indata.data:
                                words = ja_tokenize(pointdata)
                                print str(words).decode('string-escape')
                                result = []
                                listnumber = []
                                for word in words:
                                        word = word.strip()
                                        if word == "" : continue
                                        if not word in self.dic:
                                                print ("dicNoReg")
                                                continue
                                        else:
                                                num = self.dic[word]
                                        result.append(num)
                                listnumber.append(result)
                                print (listnumber)
                                if listnumber != [[]] :
                                        tokenizer = Tokenizer(num_words=max_words)
                                        print('Vectorizing sequence data...')
                                        textsmatrix = tokenizer.sequences_to_matrix(listnumber, mode='binary')
                                        ### 予測したラベルを取得
                                        predict_classes = self.loaded_model.predict_classes(textsmatrix, batch_size=batch_size)
                                        print (predict_classes)
                                        predict = self.loaded_model.predict(textsmatrix, batch_size=batch_size)
                                        print(predict)
                                        stockdata.append(str(predict_classes[0]))
                                else :
                                        stockdata.append("100")
                        systemid = "goods"
                        speechid = stockdata
                        print (systemid)
                        print (speechid)
                        ut1 = time.time()
                        print (int(ut1*100000))
                        self._SpeechManageRequire._ptr().read(systemid,speechid)	
		return RTC.RTC_OK

	###
	##
	## The aborting action when main logic error occurred.
	## former rtc_aborting_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The error action in ERROR state
	## former rtc_error_do()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The reset action that is invoked resetting
	## This is same but different the former rtc_init_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The state update action that is invoked after onExecute() action
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##

	##
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The action that is invoked when execution context's rate is changed
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK


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

def TextConceptClassifierInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=textconceptclassifier_spec)
    manager.registerFactory(profile,
                            TextConceptClassifier,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    TextConceptClassifierInit(manager)

    # Create a component
    comp = manager.createComponent("TextConceptClassifier")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

