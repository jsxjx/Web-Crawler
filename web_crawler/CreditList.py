# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import random
import time
import os



headers = {'User-Agent' : '	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',  
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Host' : 'shixin.court.gov.cn'}  
	



def getData(i):
	result=[]
	cj = cookielib.LWPCookieJar()  
	cookie_support = urllib2.HTTPCookieProcessor(cj)  
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
	urllib2.install_opener(opener)  

	postdata=urllib.urlencode({'currentPage':i})
	url = 'http://shixin.court.gov.cn/personMore.do' 
	h = urllib2.urlopen(url)  
	
	request = urllib2.Request(url, postdata,headers)  
	response = urllib2.urlopen(request).read()
	
	print u'已打开失信网页面...'
	
	soup=BeautifulSoup(response,from_encoding='utf-8')
	
	for k in soup.findAll('table',attrs={'class':'Resultlist'})[0].findAll('tr')[1:-1]:
		id=k.findAll('td')[1].a['id']		
		detailurl='http://shixin.court.gov.cn/detail?id='+id
		detail=urllib2.urlopen(detailurl).read()
		
		detail=dict(eval(detail))#不加eval这个返回的不是dict#
		
		result.append(detail)
	return result

def main():
	
	obj_fold='C:\\Python27\\creditlist\\result'
	isExists=os.path.exists(obj_fold)
	if not isExists:
		os.makedirs(obj_fold)
		print u'目录文件夹已创建！'
			
	for i in range(1,51):
		obj_file=obj_fold+'\\Page_'+str(i)+'.txt'
		isExists=os.path.exists(obj_file)
		if not isExists:
		
			namelist=getData(i)  #namelist is a list#
						
			file=open(obj_file,'w')
			for p in namelist:   #p is a dict#
					print>> file, p['iname'],' ',p['sexy'],' ',p['age'],' ',p['cardNum'],' ',p['courtName'],' ',p['publishDate']
			
			file.close()	
			print u'第 %d 页读取完毕'%i
			
	#合并所有文件#
	content=[]
	obj_file=open('C:\\Python27\\creditlist\\result\\AllPages.txt','w')
	
	for i in range(1,51):
		filepath='C:\\Python27\\creditlist\\result\\Page_'+str(i)+'.txt'
		for line in open(filepath).readlines():
			content.append(line)

	for line in content:
		obj_file.write(line)
	obj_file.close()		
			

			
			
	

if __name__ == "__main__":
	main()











