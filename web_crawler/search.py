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
import gzip


headers = {'User-Agent' : '	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',  
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Host' : 'shixin.court.gov.cn'}  
		
cj = cookielib.LWPCookieJar()  
cookie_support = urllib2.HTTPCookieProcessor(cj)  
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
urllib2.install_opener(opener)  	

def main():

	name=raw_input(u'Please input a name:').decode('gb2312').encode('utf-8')
	#测试：张全林#

	postData=urllib.urlencode({'pName':name,'pProvince':'0'})

	url='http://shixin.court.gov.cn'
	posturl = 'http://shixin.court.gov.cn/search' 
	h = urllib2.urlopen(url)  

	request = urllib2.Request(posturl, postData,headers)  
	response = urllib2.urlopen(request)
	html=response.read() 

	soup=BeautifulSoup(html,from_encoding='utf-8')
	
	targetdiv=soup.findAll('div',attrs={'id':'ResultlistBlock'})[0]
	
	numbers=len(targetdiv.findAll('tr')[1:])
	
	print u'共找到 %d 人！'%numbers
	
	for i in range(1,numbers+1):
		obj_file='result_'+str(i)+'.txt'
		file=open(obj_file,'w')
	
		id=targetdiv.findAll('tr')[i].findAll('td')[-1].a['id']
		detailurl='http://shixin.court.gov.cn/detail?id='+id
		detail=urllib2.urlopen(detailurl).read()	#返回的是json#
		detail=dict(eval(detail))#不加eval这个返回的不是dict#
		for k, v in detail.iteritems():
			print>> file, k, ' ',v
			
		file.close()
		
	

if __name__ == "__main__":
	main()










