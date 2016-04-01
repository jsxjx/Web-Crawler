# coding: utf-8

import urllib2
import cookielib
from bs4 import BeautifulSoup
import HTMLParser  
import urlparse  
import WeiboEncode
import WeiboSearch
from WeiboLogin import WeiboLogin
from WeiboUser import WeiboUser
import string  
import re 
import random
import time
import urllib
import base64
import rsa
import binascii
from WeiboFeed import WeiboFeed
import os,sys
import numpy as np
from pandas import Series, DataFrame
import pandas as pd

#txt格式转为逗号分割csv格式#
def tableToCsv(old_filepath,target_file):
	f1=file(old_filepath)
	content2=[]
	while True:	
		line=f1.readline().replace('   ',',')
		content2.append(line)
		if len(line) ==0:
			break
			
	f1.close()		
	
	f2=file(target_file,'w')
	f2.writelines(content2)	
	f2.close()	


	
def getData(key):  #传入uid或主页链接#
	keyuser=WeiboUser(key) 	
	keyuid=keyuser.uid
	keypid=keyuser.pageid
	print keyuid
	if len(keyuid)>0 and len(keypid)>0:
		obj_fold='C:\\Python27\\weibo2\\result\\'+str(keyuid)
		#----------------------------------------------------------创建用户文件夹--------------------------------------------------------------------#	
		isExists=os.path.exists(obj_fold)
		if not isExists:
			os.makedirs(obj_fold)
			print u'目录文件夹已创建！'

		#------------------------------------------------------保存基本信息(点文件)-------------------------------------------------------------#
		obj_file_path=obj_fold+'\\Basicinfomation.txt'
		if not os.path.exists(obj_file_path):
			file_6=open(obj_file_path,'w')
			print >> file_6, keyuid
			print >> file_6, keypid
			try:
				name=keyuser.username.encode('gb2312')
			except:
				name='DecodeError'				
			print >> file_6, u'用户名: '.encode('gbk'),name
			numbersresult=keyuser.get_Numbers()
			if numbersresult:
				print >> file_6, u'粉丝数、微博数、关注数: '.encode('gbk'),numbersresult[0],' ',numbersresult[1],' ',numbersresult[2]
			else:
				while True:
					print u'又冻你账号了，快去解冻我才能跑！'
			for i in keyuser.get_Info()[0]:
				try:
					i=i.encode('gbk').replace(r'rrr',' ').replace(r'rr',' ').replace(r'r',' ')
				except:
					print u'DecodeError!'
					i='NA'
				print>> file_6, i
			print u'用户信息已保存！'
			file_6.close()	
		#-----------------------------------------------------	保存头像到本地-------------------------------------------------------------------#
		obj_file_path=obj_fold+'\\'+str(keyuid)+'.png'
		if not os.path.exists(obj_file_path):
			url=keyuser.get_Photo()
			if url:
				urllib.urlretrieve(url,obj_file_path)
				print u'用户头像已保存！'	
			else:
				while True:
					print u'又冻你账号了，快去解冻我才能跑！'
					
		#---------------------------------------------------------搜索最近关注-------------------------------------------------------------------#
		obj_file_path=obj_fold+'\\Recentfollows.txt'
		if not os.path.exists(obj_file_path):
			print u'正在检索用户最近关注列表...'
			followlist=keyuser.get_follows()
			file_3=open(obj_file_path,'w')
			for i in followlist:
				print>> file_3, i.split()[0].encode('gbk'),' ',i.split()[1].encode('gbk'),' ',i.split()[2].encode('gbk')
			file_3.close()	
		#-----------------------------------------------------------搜索最近粉丝---------------------------------------------------------------#
		obj_file_path=obj_fold+'\\Recentfans.txt'
		if not os.path.exists(obj_file_path):
			print u'正在检索用户最近新添粉丝...'
			fanlist=keyuser.get_fans()
			file_5=open(obj_file_path,'w')
			for i in fanlist:
				print>> file_5, i.split()[0].encode('gbk'),' ',i.split()[1].encode('gbk'),' ',i.split()[2].encode('gbk')
			file_5.close()	
	else:
		print u'该用户不存在！'
		keyuid='NA'
		keypid='NA'
	return (keyuid,keypid)
	
def getInfoPage(key):  #传入uid或主页链接#
	keyuser=WeiboUser(key) 	
	keyuid=keyuser.uid
	keypid=keyuser.pageid
	if len(keyuid)>0 and len(keypid)>0:
		obj_fold='C:\\Python27\\weibo2\\result\\'+str(keyuid)
		#----------------------------------------------------------创建用户文件夹--------------------------------------------------------------------#	
		isExists=os.path.exists(obj_fold)
		if not isExists:
			os.makedirs(obj_fold)
			print u'目录文件夹已创建！'

		#------------------------------------------------------保存基本信息(点文件)-------------------------------------------------------------#
		obj_file_path=obj_fold+'\\Basicinfomation.txt'
		if not os.path.exists(obj_file_path):
			file_6=open(obj_file_path,'w')
			print >> file_6, keyuid
			print >> file_6, keypid
			try:
				name=keyuser.username.encode('gb2312')
			except:
				name='DecodeError'
				
			print >> file_6, u'用户名: '.encode('gbk'),name
			numbersresult=keyuser.get_Numbers()
			if numbersresult:
				print >> file_6, u'粉丝数、微博数、关注数: '.encode('gbk'),numbersresult[0],' ',numbersresult[1],' ',numbersresult[2]
			for i in keyuser.get_Info()[0]:
				try:
					i=i.encode('gbk').replace(r'rrr',' ').replace(r'rr',' ').replace(r'r',' ')
				except:
					print u'DecodeError!'
					i='NA'
				print>> file_6, i
			print u'用户信息已保存！'
			file_6.close()	
		#-----------------------------------------------------	保存头像到本地-------------------------------------------------------------------#
		obj_file_path=obj_fold+'\\'+str(keyuid)+'.png'
		if not os.path.exists(obj_file_path):
			url=keyuser.get_Photo()
			if url:
				urllib.urlretrieve(url,obj_file_path)
				print u'用户头像已保存！'	
			else:
				while True:
					print u'又冻你账号了，快去解冻我才能跑！'
		else:
			print u'该用户已存在'
	else:
		print u'该用户不存在！'
		keyuid='NA'
		keypid='NA'
		
	return (keyuid,keypid)
	
'''
getRelation这个函数：输入一个uid，遍历20页微博，找到相关账号，和之前getInfo/getData里面的账号汇总生成relationship文件。
之后将relationship里面每个账号循环读取getInfoPage/getData
每个账号是做getInfoPage还是getData循环：取决于是不是最后一轮，是的话直接用getInfoPage
'''	
def	getRelation(uid,keyuid,typ=1):    

	keyuser=WeiboUser(keyuid) 	
	keypid=keyuser.pageid	
	obj_fold='C:\\Python27\\weibo2\\result\\'+str(keyuid)	
	#-------------------------------------------用WeiboFeed类输出微博列表/和微博中转发对象id--------------------------------------------------#
	obj_fold2=obj_fold+'\\Feedlist'   
	isExists=os.path.exists(obj_fold2)
	if not isExists:
		os.makedirs(obj_fold2)
		print u'微博列表文件夹已创建！'		
	obj_fold4=obj_fold+'\\Followsearch'  
	isExists=os.path.exists(obj_fold4)
	if not isExists:
		os.makedirs(obj_fold4)
		print u'关注搜索文件夹已创建！'

	weibofeed=WeiboFeed(uid,keyuid,keypid)	
	
	p=1
	while p<=5: #最多读5页#
		obj_file_path=obj_fold2+'\\Feedlist_Page'+str(p)+'.txt'
		if not os.path.exists(obj_file_path):			
			if p==1:
				count=1
			else:		
				count=open(obj_fold2+'\\Feedlist_Page'+str(p-1)+'.txt').readlines()[-1].split()[0]
				count=int(count)	
				
			#调用weibofeed类#
			mid,feedcontent,numbers,followsearch,posttime = weibofeed.feedlist(p)	
			
			if mid==[]:
				break				
			file_1=open(obj_file_path,'w')
			print>> file_1,u'编号'.encode('gb2312'),' ',u'微博ID'.encode('gb2312'),' ',u'发表时间'.encode('gb2312'),' ',u'微博正文'.encode('gb2312'),' ',u'评论数'.encode('gb2312'),' ',u'转发数'.encode('gb2312'),' ',u'点赞数'.encode('gb2312'),'\n'			
			rand=random.randint(1, 5)
			time.sleep(rand)		
			i=1 
			while i<= len(mid):
				try:
					print feedcontent[i-1]
				except:
					pass
				try:
					print>>file_1, count,' ',mid[i-1],' ',posttime[i-1],' ',feedcontent[i-1].encode('gb2312'),' ',numbers[i-1]			
				except:	
					try:
						print>>file_1, count,' ',mid[i-1],' ',posttime[i-1],' ','DecodeError',' ',numbers[i-1]	
					except:
						pass
					print u'UnicodeEncodeError Notice!'
				i+=1
				count+=1
						
			file_2=open(obj_fold4+'\\Followsearch_Page'+str(p)+'.txt','w') #保存微博中关注人目标文件#
			for i in followsearch:	
				print>> file_2, i.split()[0].encode('gbk'),' ',i.split()[1].encode('gbk'),' ',i.split()[2].encode('gbk'),' ',i.split()[3].encode('gbk'),' ',i.split()[4].encode('gbk')
			
			print u'第 %d 页已保存！'%p
			file_1.close()
			file_2.close()	
		p+=1
			
	#---------------------------------------------汇总搜索结果到searchResult：id 名称 时间 链接   类型（三种来源）--------------------------------#
	obj_file_path=obj_fold+'\\searchResult.txt'
	if not os.path.exists(obj_file_path):		
		searchResult=[]
		obj_fold_2=obj_fold+'\\Followsearch\\'
		files = os.listdir(obj_fold_2) 
		for file in files:
			lines=open(obj_fold_2+file).readlines()
			for line in lines:
				line=line.replace('\n','')
				pattern=re.compile(' \d{2}:\d{2} ')
				line = re.sub(pattern, '', line) #去掉时间中的分钟#
				line=line.replace('     ','   ').replace('    ','   ')
				searchResult.append(line+'   1')  
		print u'Followsearch 汇总完毕！'		
	
		obj_file=obj_fold+'\\Recentfollows.txt'
		for line in open(obj_file).readlines():
			line=('Recent   '+line).replace(' 0','').replace('\n','')
			line=line.replace('     ','   ').replace('    ','   ')
			searchResult.append(line+'   2')  
		print u'最近关注 汇总完毕！'
		
		obj_file=obj_fold+'\\Recentfans.txt'
		for line in open(obj_file).readlines():
			line=('Recent   '+line).replace(' 0','').replace('\n','')
			line=line.replace('     ','   ').replace('    ','   ')
			searchResult.append(line+'   3')  
		print u'最近粉丝 汇总完毕！'
		
		file_7=open(obj_file_path,'w')
		print>> file_7, 'Time'+'   '+'ID'+'   '+'Name'+'   '+'Link'+'   '+'Type'
		for s in searchResult:
			print>> file_7, s
		file_7.close()
		print u'关系搜索结果已保存在searchResult.txt!'	
		
	#---------------------------------------------初步统计频数、unique到relationship文件-------------------------------------------#
	if not os.path.exists(obj_fold+'\\relationships.csv'):	
		if not os.path.exists(obj_fold+'\\searchResult.csv'):	
			tableToCsv(obj_fold+'\\searchResult.txt',obj_fold+'\\searchResult.csv')
				
		df_1=pd.read_csv(obj_fold+'\\searchResult.csv') 
		nameCount=DataFrame(df_1['Name'].value_counts())  
		nameCount.to_csv(obj_fold+'\\nameCount.csv') 
		df_2=pd.read_csv(obj_fold+'\\nameCount.csv',header=None,names=['Name','Count'])
		merged=pd.merge(df_1,df_2,on='Name').sort_index(by=['Name','Time']).reindex(range(len(df_1['Name']))) 
		Relationtable=merged.groupby(['Name']).first()
		Relationtable.to_csv(obj_fold+'\\relationships.csv')
		
	#-----------------------------------------------第一次大循环，循环getInfoPage或者getData----------------------------------------------#
	if os.path.exists(obj_fold+'\\relationships.csv'):
		file=open(obj_fold+'\\relationships.csv')
		numberofLoop=len(file.readlines())-1
		print u'一共需要读取 %d 人！' %numberofLoop
		na={'Name ':[' ']}
		df=pd.read_csv(obj_fold+'\\relationships.csv',na_values=na).dropna()
		
	if not os.path.exists(obj_fold+'\\edges.csv'):	#如果是第一次读#
		file=open(obj_fold+'\\edges.csv','w')  	
		file.write('Source'+','+'To'+','+'Time'+','+'Count'+','+'Pid'+','+'Type'+'\n')
		for i in range(0,numberofLoop):
			try:
				id=str(df.ix[i,'ID'])
				if id.isdigit():
					if typ==1:
						ids=getData(id)	
					elif typ==2:
						ids=getInfoPage(id)	
				else:
					url=df.ix[i,'Link']			
					if typ==1:
						ids=getData(url)					
					elif typ==2:
						ids=getInfoPage(url)
						
				type=str(df.ix[i,'Type'])
				
				file.write(str(keyuid)+','+str(ids[0])+','+df.ix[i,'Time']+','+str(df.ix[i,'Count'])+','+str(ids[1])+','+type+'\n')	
			except:
				file.write('\n')
		print u'信息读取完毕！'		
		file.close()
		
	else:  #如果不是第一次#
		file=open(obj_fold+'\\edges.csv')
		currentNumber=len(file.readlines())-1  #已经读到了第几人#
		print u'已经读取了%d 人!'%currentNumber 
		file=open(obj_fold+'\\edges.csv','a')	
		for i in range(currentNumber,numberofLoop):
			try:
				id=str(df.ix[i,'ID'])
				if id.isdigit():
					if typ==1:
						ids=getData(id)	
					elif typ==2:
						ids=getInfoPage(id)	
				else:
					url=df.ix[i,'Link']			
					if typ==1:
						ids=getData(url)	
					elif typ==2:
						ids=getInfoPage(url)
				type=str(df.ix[i,'Type'])					
				file.write(str(keyuid)+','+str(ids[0])+','+df.ix[i,'Time']+','+str(df.ix[i,'Count'])+','+str(ids[1])+','+type+'\n')
			except:
				file.write('\n')
		print u'信息读取完毕！'
		
		file.close()
		try:
			os.remove(obj_fold+'\\nameCount.csv')
			os.remove(obj_fold+'\\searchResult.csv')
			os.remove(obj_fold+'\\searchResult.csv')
		except:
			pass
			
def main():
	keyuid=10503   #在这里修改起始用户 TimYang，新浪微博技术总监#

	#--------------------------------------------------------- 登陆微博-----------------------------------------------------------------------#
	userlists=open('userlists.txt').readlines() 
	rand=0
	username=userlists[rand].split()[0]
	print username
	password=userlists[rand].split()[1]
	uid=userlists[rand].split()[2]	
	
	weibologin=WeiboLogin(username,password)
	
	if weibologin.Login()==True:
		print u"登录成功!"
	else:
		print u'登陆失败！'
		
	file_user=open('log_id.txt','w')
	print>> file_user,uid
	file_user.close()

	#------------------------------------------创建好用户文件夹，获得基本信息-----------------------------------------------------------------#	
	obj_fold='C:\\Python27\\weibo2\\result\\'+str(keyuid)
	obj_file_path=obj_fold+'\\Recentfans.txt'
	if not os.path.exists(obj_file_path):
		 getData(keyuid)
	
	#-----------------------------------------读微博，创建关系文件，遍历相关id 11页------------------------------------------------------------#
	getRelation(uid,keyuid)	
	#-------------------------------------读相关id微博，创建相关id关系文件，遍历相关id主页-----------------------------------------------------#
	if os.path.exists(obj_fold+'\\edges.csv'):
		file=open(obj_fold+'\\edges.csv')

		na={'To':['NA']}
		df=pd.read_csv(obj_fold+'\\edges.csv',na_values=na).dropna()
		df.to_csv(obj_fold+'\\edges_nadrop.csv')
		df=pd.read_csv(obj_fold+'\\edges_nadrop.csv')  #这是个临时文件，只用来读id#
		numberofLoop=len(df.values)
		print u'共有 %d 位有效用户！' %numberofLoop
	
		if not os.path.exists(obj_fold+'\\records.txt'):
			file_write=open(obj_fold+'\\records.txt','w') #以及我怎么知道读到了第几个？？？#
			frompage=0
		else:
			file_for_records=obj_fold+'\\records.txt'
			frompage=len(open(file_for_records).readlines())
			file_write=open(file_for_records,'a')
			
		for i in range(frompage,numberofLoop):  #每个需要读微博，创建edge的id#
			id=str(df.ix[i,'To'])
			n=id.find('.')
			id=id[:n]
			print u'正在读id %s'%id
			obj_fold_son='C:\\Python27\\weibo2\\result\\'+id
			if os.path.exists(obj_fold_son):
			
				getRelation(uid,id,typ=2)  #先读微博，生成relationship文件，他的相关用户id我只要主页信息，所以typ=2#
				
				print>> file_write, id
				
			else:
				print u'用户目录文件夹不存在！'
		file_write.close()
		
if __name__=='__main__':	
    main()	


	