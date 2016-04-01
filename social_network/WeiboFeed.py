# coding: utf-8
'''
weibo feedlist

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

class WeiboFeed:
	def __init__(self,uid,userID, pageID): #需要我登陆时候的uid#
		self.uid=userID
		self.pageid=pageID
		self.weiboPage='http://weibo.com/p/'+self.pageid+'/home?'		
		self.domain=pageID[0:6]

	def feedlist(self,Page): #读取第page页上的微博列表#
		Page=str(Page)
		feedcontent=[]	#存放微博内容#
		feedmid=[] #存放微博id#
		numbers=[] #存放三个数据#
		posttime=[] #存放post时间 来自#
		followsearch=[] #存放微博正文中读到的相关可能关注#
		
		url=self.weiboPage+'&is_search=0&visible=0&is_tag=0&profile_ftype=1&page='+Page+'#feedtop'
		#形如：http://www.weibo.com/p/1005051883627565/home?pids=Pl_Official_MyProfileFeed__22&is_search=0&visible=0&is_tag=0&profile_ftype=1&page=3#feedtop#
		urlcontent=urllib2.urlopen(url).read()
		print u'正在读取第%s页...'%Page
		lines=urlcontent.splitlines()
		for line in lines: 		
			if line.startswith('<script>FM.view({"ns":"pl.content.homeFeed.index","domid":"Pl_Official_MyProfileFeed__'):
				p=line.find('Pl_Official_MyProfileFeed__')
				self.pids=filter(lambda x:x.isdigit(),line[p+27:p+30])				
				n = line.find('html":"')  		
				if n>0 : 		
					j = line[n+7: -12].replace("\\n", "")  
					j = j.replace("\\t","").replace("\\",'')  				
					soup_1=BeautifulSoup(j,from_encoding='utf-8')
					try:
						mid=soup_1.findAll('div',attrs={'class':'WB_cardwrap WB_feed_type S_bg2 '})[0]['mid']
						#http://www.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&pids=Pl_Official_MyProfileFeed__22&is_search=0&visible=0&is_tag=0&profile_ftype=1&page=1&pre_page=1&max_id=&end_id=3819354795897409&pagebar=0&filtered_min_id=&pl_name=Pl_Official_MyProfileFeed__22&id=1005051883627565&script_uri=/p/1005051883627565/home&feed_type=0&domain_op=100505&__rnd=1428649169317#
						
						#第一次异步加载#
						randtime=str(time.time()).replace('.','')
						url='http://www.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain='+self.domain+'&pids='+self.pids+'&is_search=0&visible=0&is_tag=0&profile_ftype=1&page='+Page+'&pre_page='+Page+'&max_id=&end_id='+mid+'&pagebar=0&filtered_min_id=&pl_name='+self.pids+'&id='+self.pageid+'&script_uri=/p/'+self.pageid+'/home&feed_type=0&domain_op='+self.domain+'&__rnd='+str(randtime)
						
						urlcontent=urllib2.urlopen(url).read()
						n = urlcontent.find('data":"')
						if n>0: 
							print u'正在加载余下内容。。。'
							j = urlcontent[n+7: -3] 
							j = j.replace("\\n",'').replace('\\t','').replace('\\"','\"').replace('\\/','/')
							soup_2=BeautifulSoup(j)
							
						
							#http://www.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&pids=Pl_Official_MyProfileFeed__22&is_search=0&visible=0&is_tag=0&profile_ftype=1&page=1&pre_page=1&max_id=&end_id=3819354795897409&pagebar=1&filtered_min_id=&pl_name=Pl_Official_MyProfileFeed__22&id=1005051883627565&script_uri=/p/1005051883627565/home&feed_type=0&domain_op=100505&__rnd=1428650019213#
							
							#第二次异步加载#					
							randtime=str(time.time()).replace('.','')
							url='http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain='+self.domain+'&is_search=0&visible=0&is_tag=0&profile_ftype=1&page='+Page+'&pre_page='+Page+'&max_id=&end_id='+mid+'&pagebar=0&filtered_min_id=&pl_name='+self.pids+'&id='+self.pageid+'&script_uri=/p/'+self.pageid+'/home&feed_type=0&domain_op='+self.domain+'&__rnd='+str(randtime)
							urlcontent2=urllib2.urlopen(url).read()
							if urlcontent2==urlcontent:
								soups=[soup_1,soup_2]
								print u'第二次异步加载未完成！'
							else:
								n = urlcontent2.find('data":"')
								if n>0: 
									print u'正在加载余下内容。。。'
									j = urlcontent2[n+7: -3] 
									j = j.replace("\\n",'').replace('\\t','').replace('\\"','\"').replace('\\/','/')
									soup_3=BeautifulSoup(j)
									soups=[soup_1,soup_2,soup_3]						
								
							flag=0 #异步加载后编码不同#
							for soup in soups:
								for d in soup.findAll('div',attrs={'class':'WB_cardwrap WB_feed_type S_bg2 '}):
									if d.findAll(attrs={'class':'WB_detail'}):
										main=d.findAll('div',attrs={'class':'WB_detail'})[0].findAll('div',attrs={'class':'WB_from S_txt2'})[0]
										
										href='http://weibo.com'+main.a['href'] #提取每条微博主页#
										weibotime=main.a['title']
										mid=d['mid']  #提取每条微博id#
										posttime.append(weibotime)#微博时间#	
										feedmid.append(mid)
										
										#评论转发点赞数#
										if flag==0:
											commentNum=d.findAll('span',attrs={'node-type':'comment_btn_text'})[0].string.replace(u'\u8bc4\u8bba','')
											repostNum=d.findAll('span',attrs={'node-type':'forward_btn_text'})[0].string.replace(u'\u8f6c\u53d1','')
											
										if flag==1:
											commentNum=d.findAll('span',attrs={'node-type':'comment_btn_text'})[0].string.replace('\u8bc4\u8bba','')
											repostNum=d.findAll('span',attrs={'node-type':'forward_btn_text'})[0].string.replace('\u8f6c\u53d1','')
											
										likeNum=d.findAll('span',attrs={'node-type':'like_status'})[0].em.string
										if commentNum:
											pass
										else:
											commentNum=0																			
										if repostNum:
											pass
										else:
											repostNum=0									
										if likeNum:
											pass
										else:
											likeNum=0	
											
										add=str(commentNum)+' '+str(repostNum)+' '+str(likeNum)
										numbers.append(add)
											
										#内容，可能会有编码问题#
										#对于每条微博的主要div#
										maindiv=d.findAll('div',{'class','WB_detail'})[0]
										contentdiv=maindiv.findAll('div',attrs={'node-type':'feed_list_content'})[0]
										divcontent=str(contentdiv)
										content=contentdiv.get_text()#这里的content可能包括转发前其他用户的转发#
										n= content.find('//')
										l=divcontent.find(r'//')
										m=divcontent.find(r'<a')
										#1是转发#
										if maindiv.findAll('div',attrs={'class':'WB_feed_expand'}) and n==-1:
											try:								
												forwardiddiv=maindiv.findAll('div',attrs={'class':'WB_feed_expand'})[0].findAll('div',attrs={'class':'WB_info'})[0]
												forwardid1=forwardiddiv.a['usercard'].replace('id=','').replace('name=','')
												forwardhref1=('http://www.weibo.com'+forwardiddiv.a['href']).replace('http://www.weibo.comhttp://weibo.com','http://www.weibo.com')
												try:
													forwardname1=forwardiddiv.a['title']
												except:
													forwardname1=forwardid
												if flag==0:
													followsearch.append(weibotime+' '+forwardid1+' '+forwardname1+' '+forwardhref1+' 1')
												else:
													forwardid1=forwardid1.decode("unicode-escape")
													forwardname1=forwardname1.decode("unicode-escape")
													followsearch.append(weibotime+' '+forwardid1+' '+forwardname1+' '+forwardhref1+' 1')
												forwardid1,forwardname1,forwardhref1='','',''
											except:
												pass
											#转发了多次转发的内容，提取直接转发对象的id#
										
										if n!=-1:
											content=content[:n] #这时的content只包含了原创#
											try:
												forwardid2=maindiv.a['usercard'].replace('id=','').replace('name=','')
												forwardhref2=('http://www.weibo.com'+maindiv.a['href']).replace('http://www.weibo.comhttp://weibo.com','http://www.weibo.com')
												try:
													forwardname2=maindiv.a['title']
												except:
													forwardname2=forwardid2
												if flag==0:
													followsearch.append(weibotime+' '+forwardid2+' '+forwardname2+' '+forwardhref2+' 1')
												else:
													forwardid2=forwardid2.decode("unicode-escape")
													forwardname2=forwardname2.decode("unicode-escape")
													followsearch.append(weibotime+' '+forwardid2+' '+forwardname2+' '+forwardhref2+' 1')
												forwardid2,forwardname2,forwardhref2='','',''
											except:
												pass
										
										#2 原创内容中at了别人#
										if m!=-1 and l!=-1 and m<l:
											for aa in contentdiv.findAll('a'):
												if aa.has_attr('usercard'):		
													try:
														forwardid3=aa['usercard'].replace('id=','').replace('name=','')
														forwardhref3=('http://www.weibo.com'+aa['href']	).replace('http://www.weibo.comhttp://weibo.com','http://www.weibo.com')								
														try:
															forwardname3=aa['title']
														except:
															forwardname3=forwardid3
													except:
														pass
													if flag==0:
														followsearch.append(weibotime+' '+forwardid3+' '+forwardname3+' '+forwardhref3+' 2')
													else:
														forwardid3=forwardid3.decode("unicode-escape")
														forwardname3=forwardname3.decode("unicode-escape")
														followsearch.append(weibotime+' '+forwardid3+' '+forwardname3+' '+forwardhref3+' 2')
													forwardid3,forwardname3,forwardhref3='','',''
															
														
										#保存提取到的content#
										if content and flag==0:
											content=content.replace('                                    ','')
											feedcontent.append(content)
										elif content and flag==1:
											content=content.replace('                                    ','').decode("unicode-escape")
											feedcontent.append(content)
									else:
										print u'没有找到微博！'
								flag=1	
					except:
						pass
		return (feedmid,feedcontent,numbers,followsearch,posttime)
	
	def likeidSearch(self,mid):
		likeidlist=[]
		randtime=str(time.time()).replace('.','')
		url='http://weibo.com/aj/v6/like/small?ajwvr=6&mid='+mid+'&&location=page_'+self.domain+'_single_weibo&__rnd='+randtime
		urlcontent=urllib2.urlopen(url).read()
		n=urlcontent.find('"html":"')
		if n>0: 
			print u'正在读取点赞用户。。。'
			j = urlcontent[n+9: -3] 
			j = j.replace("\\n",'').replace('\\t','').replace('\\"','\"').replace('\\/','/')
			soup=BeautifulSoup(j)	
			
			for k in soup.findAll('li'):
				try:
					idadd=k['uid']
					nameadd=k.a.img['title'].decode("unicode-escape")
					hrefadd=k.a['href']			
				except:
					idadd=''
					nameadd=''
					hrefadd=''
				likeidlist.append(idadd+' '+nameadd+' '+hrefadd)
		return likeidlist
							
				
	def commentidSearch(self,mid,uid): 	
		commentidlist=[]
		randtime=str(time.time()).replace('.','')
		url='http://weibo.com/aj/v6/comment/big?ajwvr=6&mid='+mid+'&id='+mid+'&filter=hot&__rnd='+randtime #热门评论#
		#http://weibo.com/aj/v6/comment/big?ajwvr=6&mid=3826228143912936&id=3826228143912936&filter=hot&__rnd=1429368258300#
		urlcontent=urllib2.urlopen(url).read()
		
		n=urlcontent.find('"html":"')
		if n>0: 
			print u'正在读取评论用户。。。'
			j = urlcontent[n+9: -3] 
			j = j.replace("\\n",'').replace('\\t','').replace('\\"','\"').replace('\\/','/')
			soup=BeautifulSoup(j)	
			
			for k in soup.findAll('div',attrs={'class':'list_li S_line1 clearfix'}):
				try:
					idadd=k.findAll('div',attrs={'class','WB_text'})[0].a['usercard'].replace('id=','').replace('name=','')
					nameadd=k.findAll('div',attrs={'class','WB_text'})[0].a.string.decode("unicode-escape")
					hrefadd=k.findAll('div',attrs={'class','WB_text'})[0].a['href']					
				except :
					print u'未知错误！'
					idadd=''
					nameadd=''
					hrefadd=''
				if idadd!=uid:  #自己回复评论不包括#
					commentidlist.append(idadd+' '+nameadd+' '+hrefadd)
		return commentidlist
	
	def repostidSearch(self,mid): 
		repostidlist=[]
		randtime=str(time.time()).replace('.','')
		url='http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id='+mid+'&__rnd='+randtime
		urlcontent=urllib2.urlopen(url).read()
		
		n=urlcontent.find('"html":"')
		if n>0: 
			print u'正在读取转发用户。。。'
			j = urlcontent[n+9: -3] 
			j = j.replace("\\n",'').replace('\\t','').replace('\\"','\"').replace('\\/','/')
			soup=BeautifulSoup(j)	
			
			for k in soup.findAll('div',attrs={'class':'list_li S_line1 clearfix'}):
				try:
					idadd=k.findAll('div',attrs={'class','WB_text'})[0].a['usercard'].replace('id=','')
					nameadd=k.findAll('div',attrs={'class','WB_text'})[0].a.string.decode("unicode-escape")
					hrefadd=k.findAll('div',attrs={'class','WB_text'})[0].a['href']
				except :
					print u'未知错误！'
					idadd=''
					nameadd=''
					hrefadd=''
				repostidlist.append(idadd+' '+nameadd+' '+hrefadd)
				
		return repostidlist
		
		
		
