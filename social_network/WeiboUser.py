# coding: utf-8
'''
user info

'''

import urllib2
import cookielib
from bs4 import BeautifulSoup
import HTMLParser  
import urlparse 
import string  
import re 
import random
import time
import urllib
import base64
import rsa
import binascii

class WeiboUser:  #可以传入uid，或者一个主页链接（1，可以直接在后面加info？转到info页，2，需要打开链接提取uid再转到info页的）#

	def __init__(self, userID):
	
		userID=str(userID)
		self.uid=''
		self.username=''
		self.pageid=''
		
		if userID.isdigit(): #若传入的是uid#
			print u'传入的是uid，可用！'
			self.uid=str(userID)
			url='http://weibo.com/'+str(self.uid)+'/info?'
			content=urllib2.urlopen(url).read()
			self.lines=content.splitlines()	
			
		elif userID.find('from=feed&loc=at')>0: #如果传入的是主页链接，必须先打开主页#
			url=userID
			content=urllib2.urlopen(url).read()
			print u'传入的是中文主页链接，需要额外打开一个网页！'
			self.lines=content.splitlines()
			#找uid#
			for line in self.lines: 	
				if line.startswith('$CONFIG[\'oid\']='): 
					n = line.find('=')  		
					if n>0: 		
						self.uid = line[n+2: -3]
						url='http://weibo.com/'+str(self.uid)+'/info?'
						content=urllib2.urlopen(url).read()	
						self.lines=content.splitlines()
						print u'定位成功'
										
		elif userID.find('u/')>0:	#如果传入的链接要去掉u加info打开#
			n=userID.find('u/')
			url=userID[:n-1]+userID[n+2:]+'/info?'
			print url
			content=urllib2.urlopen(url).read()	
			print u'传入的是u+数字用户链接，可用！'
			self.lines=content.splitlines()
			#找uid#
			for line in self.lines: 		
				if line.startswith('$CONFIG[\'oid\']='): 
					n = line.find('=')  		
					if n>0: 	
						print u'已找到uid！'
						self.uid = line[n+2: -3]

		else:   #如果传入的链接可以直接加info打开#
			url=userID+'/info?'
			print url
			content=urllib2.urlopen(url).read()	
			print u'传入链接可用！'
			self.lines=content.splitlines()
			#找uid#
			for line in self.lines: 		
				if line.startswith('$CONFIG[\'oid\']='): 
					n = line.find('=')  		
					if n>0: 
						print u'已找到uid！'
						self.uid = line[n+2: -3]
						
		#找到page id#
		for line in self.lines: 
			if line.startswith('$CONFIG[\'page_id\']='): 
				n = line.find('=')  		
				if n>0: 		
					self.pageid = line[n+2: -3]
					self.weiboPage='http://weibo.com/p/'+str(self.pageid)+'/home?'
					self.followPage='http://weibo.com/p/'+str(self.pageid)+'/follow?'		
					self.fanPage='http://weibo.com/p/'+str(self.pageid)+'/follow?relate=fans'
				
		#找到username#
			if line.startswith('$CONFIG[\'onick\']='): 
				n = line.find('=')  		
				if n>0: 		
					self.username = line[n+2: -3].decode('utf-8')	#可能存在解码问题#
					
	def get_Photo(self):
		url=[]
		for line in self.lines:
			if line.startswith('<script>FM.view({"ns":"pl.header.head.index","domid":"Pl_Official_Headerv6__'):
				n = line.find('html":"')  
				if n>0: 			
					j = line[n+7: -12].replace("\\n", "").replace("\\t","").replace("\\",'') 			
					soup=BeautifulSoup(j,from_encoding='utf-8') 
					if soup.findAll('p',attrs={'class':'photo_wrap'}):
						url=soup.findAll('p',attrs={'class':'photo_wrap'})[0].img['src']
				break
		return url
		
	def get_Info(self):
		basicinfo=[]
		intro=[]
		for line in self.lines:
			if line.startswith('<script>FM.view({"ns":"pl.header.head.index","domid":"Pl_Official_Headerv6__'):
				n = line.find('html":"')  
				if n>0: 			
					j = line[n+7: -12].replace("\\n", "").replace("\\t","").replace("\\",'') 			
					soup=BeautifulSoup(j,from_encoding='utf-8') 
					if soup.findAll('div',attrs={'class':'pf_intro'}):
						intro=soup.findAll('div',attrs={'class':'pf_intro'})[0].string
						try:
							basicinfo.append(intro+' ')
						except:
							pass
			if line.startswith('<script>FM.view({"ns":"","domid":"Pl_Official_PersonalInfo__'):
				n = line.find('html":"')  
				if n>0: 			
					j = line[n+7: -12].replace("\\n", "").replace("\\t","").replace("\\",'') 			
					soup=BeautifulSoup(j,from_encoding='utf-8') 
					if soup.findAll('div',attrs={'class':'WB_cardwrap S_bg2'}):
						for k in soup.findAll('div',attrs={'class':'WB_cardwrap S_bg2'}):
							for l in k.findAll('li'):
								try:
									basicinfo.append(l.get_text()+' ')
								except:
									pass
			
		return 	basicinfo,intro
		
		
	def get_Numbers(self):
		number=[]#粉丝数、微博数、关注数#	
		for line in self.lines: 									
			if line.startswith('<script>FM.view({"ns":"","domid":"Pl_Core_T8CustomTriColumn__'):  #如果打开的是info主页#
				n = line.find('html":"')  
				if n>0: 			
					j = line[n+7: -12].replace("\\n", "").replace("\\t","").replace("\\",'')    

					soup=BeautifulSoup(j,from_encoding='utf-8')  
					for k in soup.findAll('div',attrs={'class':'WB_innerwrap'})[0].findAll('strong'):
						number.append(k.string+' ')
					if len(number)==3:	
						print u'该用户共关注了%s人，有粉丝%s名，微博%s条'%(number[0],number[1],number[2])
					else:
						print u'未知错误！'
		return number			

	def followPageNum(self): 
		followPageContent=urllib2.urlopen(self.followPage).read() 
		lines=followPageContent.splitlines()
		for line in lines:
			if line.startswith('<script>FM.view({"ns":"pl.content.followTab.index","domid":"Pl_Official_HisRelation__'):
				n = line.find('html":"')  
				if n > 0: 
					j = line[n+7: -12].replace("\\n", "").replace("\\t","").replace("\\",'')   
					soup=BeautifulSoup(j,from_encoding='utf-8')
					totalPageNumber=int(soup.findAll('div',{'class','W_pages'})[0].findAll('a')[-1].string)
					print u'该用户共关注了%d页用户！'%totalPageNumber
					return totalPageNumber
					
	def fanPageNum(self): 
		fanPageContent=urllib2.urlopen(self.fanPage).read() 
		lines=fanPageContent.splitlines()
		for line in lines:
			if line.startswith('<script>FM.view({"ns":"pl.content.followTab.index","domid":"Pl_Official_HisRelation__'):
				n = line.find('html":"')  
				if n > 0: 
					j = line[n+7: -12].replace("\\n", "").replace("\\t","").replace("\\",'')   
					soup=BeautifulSoup(j,from_encoding='utf-8')
					totalPageNumber=int(soup.findAll('div',{'class','W_pages'})[0].findAll('a')[-1].string)
					print u'该用户共有%d页粉丝！'%totalPageNumber
					return totalPageNumber
							
	
	def get_follows(self,PageNumber=5):
		f=0 #第一次和之后的url地址不一样#
		e=0 #是否已经发生错误#
		followlist=[]
		pids=''
		for i in range(1,PageNumber+1):	
			if f==0:
				print u'第一次读关注'
				url='http://weibo.com/p/'+self.pageid+'/follow?page='+str(i)
				urlcontent=urllib2.urlopen(url).read()

			elif e==0:
				url2='http://weibo.com/p/'+self.pageid+'/follow?&page='+str(i)+'#'+pids
				urlcontent2=urllib2.urlopen(url2).read()
				if urlcontent2==urlcontent:
					e=1
					print u'页面内容重复！'
				else:
					urlcontent=urlcontent2
			if e==0:
				lines=urlcontent.splitlines()
				print u'正在读取关注列表第 %d 页..'%i
				e=1
				for line in lines:
					if line.startswith('<script>FM.view({"ns":"pl.content.followTab.index","domid":"Pl_Official_HisRelation__') : 
						n = line.find('html":"')
						point=line.find('"Pl_Official_HisRelation__')
						pids=line[point+1:point+28]
						if n > 0: 	
							j = line[n+7:-12].replace("\\n", "").replace("\\t","").replace("\\",'')    
							
							soup=BeautifulSoup(j,from_encoding='utf-8') 
							
							for k in soup.findAll('div',attrs={'class':'info_name W_fb W_f14'}):
								try:
									name=k.findAll('a')[0].string
									id=k.a['usercard'].replace('id=','').replace('usercard=','')
									href='http://www.weibo.com'+k.a['href']
									print u'当前用户最近关注了 %s！'%name
									if name:
										followlist.append(id+' '+name+' '+href)
									e=0
								except:
									print u'未知错误！'												
			f=1
			rd=random.randint(1, 3)	
			time.sleep(rd)							
		return followlist
		
	def get_fans(self,PageNumber=5):
		f=0 #第一次和之后的url地址不一样#
		e=0
		pids=''
		fanlist=[]
		for i in range(1,PageNumber+1):	
			if f==0:
				url='http://weibo.com/p/'+self.pageid+'/follow?relate=fans&page='+str(i)
				urlcontent=urllib2.urlopen(url).read()
			elif e==0:
				url='http://weibo.com/p/'+self.pageid+'/follow?relate=fans&page='+str(i)+'#'+pids
				urlcontent2=urllib2.urlopen(url).read()
				if urlcontent2==urlcontent:
					e=1
				else:
					urlcontent=urlcontent2
			if e==0:
				e=1
				lines=urlcontent.splitlines()
				print u'正在读取粉丝列表第%d页'%i
				for line in lines:
					if line.startswith('<script>FM.view({"ns":"pl.content.followTab.index","domid":"Pl_Official_HisRelation__'): 
						n = line.find('html":"')
						point=line.find('"Pl_Official_HisRelation__')
						pids=line[point+1:point+28]
						if n > 0: 	
							j = line[n+7:-12].replace("\\n", "").replace("\\t","").replace("\\",'')    
							soup=BeautifulSoup(j,from_encoding='utf-8') 
							
							for k in soup.findAll('div',attrs={'class':'info_name W_fb W_f14'}):
								try:
									name=k.findAll('a')[0].string
									id=k.a['usercard'].replace('id=','').replace('name=','')
									href='http://www.weibo.com'+k.a['href']
									print u'用户 %s 关注了当前用户！'%name	
									e=0
								except:
									print u'未知错误！'
								if name:
									fanlist.append(id+' '+name+' '+href)						
				rd=random.randint(1, 3)	
				time.sleep(rd)	
			f=1
		return fanlist
		
	def get_groups():
		pass

