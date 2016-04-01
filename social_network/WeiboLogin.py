# coding: utf-8
import cookielib

import WeiboEncode
import WeiboSearch

import urllib
import urllib2
import base64
import rsa
import binascii

class WeiboLogin:
	def __init__(self, user, pwd, enableProxy = False):
		
		print u"初始化登陆..."
		self.userName = user
		self.passWord = pwd
		self.enableProxy = enableProxy
        #用于登陆的第一步（获取servertime、nonce等)
		self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683"
		self.loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
		self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}
		
	def Login(self):
		self.EnableCookie(self.enableProxy)#cookie或代理服务器配置        
		serverTime, nonce, pubkey, rsakv = self.GetServerTime()#登陆的第一步：访问新浪服务器得到serverTime等信息，然后利用这些信息加密用户名和密码，构建POST请求
		postData = WeiboEncode.PostEncode(self.userName, self.passWord, serverTime, nonce, pubkey, rsakv)#加密用户和密码
		print "Post data length:", len(postData)
		req = urllib2.Request(self.loginUrl, postData, self.postHeader)
		print u"正在发送请求..."
		result = urllib2.urlopen(req)#登陆的第二步——向self.loginUrl发送用户和密码，得到重定位信息后，解析得到最终跳转到的URL，打开该URL后，服务器自动将用户登陆信息写入cookie，登陆成功。
		text = result.read()
		try:
			loginUrl = WeiboSearch.sRedirectData(text)#解析重定位结果
			urllib2.urlopen(loginUrl)
		except:
			print u'登陆出错!'
			return False
		return True
		
	def GetServerTime(self):
		"Get server time and nonce, which are used to encode the password"  
		print u"正在获取服务器数据..."
		serverData = urllib2.urlopen(self.serverUrl).read()#得到网页内容
		print serverData

		try:
			serverTime, nonce, pubkey, rsakv = WeiboSearch.sServerData(serverData)#解析得到serverTime，nonce等
			return serverTime, nonce, pubkey, rsakv
		except:
			print u'获取服务器数据出错！'
			return None
	
	def EnableCookie(self, enableProxy):
		import urllib2
		"用于设置cookie及代理服务器."
		cookiejar = cookielib.LWPCookieJar()#建立cookie
		cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
		if enableProxy:
			proxy_support = urllib2.ProxyHandler({'http':'http://122.96.59.107:843'})#使用代理
			opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
			print u"正在使用代理"
		else:
			opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
		urllib2.install_opener(opener)#构建cookie对应的opener


