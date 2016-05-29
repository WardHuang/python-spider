#coding=utf-8

import re
import urllib
import urllib2
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" ) #避免response.read().decode('utf-8') 报错

class TXZP(object):
	"""
	docstring for TXZP
	#http://hr.tencent.com/position.php?keywords=&lid=0&tid=87
	#baseurl = 'http://hr.tencent.com/position.php?tid=0&lid=0&keywords=&start='
	#Tech = 'tid='
	#City = 'lid='
	#PageNum = 循环因子
	#MidLink = 
	#Lastlink = '0#a'
	#ConStr = '&'

	"""
	def __init__(self, BaseUrl,LastLink):
		'''
		这是初始化函数
		'''
		super(TXZP, self).__init__()
		self.BaseUrl = BaseUrl
		self.Lastlink = Lastlink

	def getContent(self,PageNum):
		'''
		这是获取整个网页的内容
		@PageNum是页数，招聘信息的页数 是 url 的 start后的数值 + 1
		'''
		try:
			Url = BaseUrl + str(PageNum) + Lastlink # 获取整个URL
			request = urllib2.Request(Url)			#利用urllib2的库来获取网页的内容
			response = urllib2.urlopen(request)
			return response.read().decode('utf-8')
		except urllib2.URLError,e:                  #访问失败，抛出异常
			if hasattr(e,"reason"):
				print u"connect error , the reason is ",e.reason
				return None

	def getStr(self,Outstr,FileHandle):             #得到要抓取的内容，并写入文件
		pattern = re.compile('<tr\sclass="\w{3,4}">.*?</tr>',re.S)  #爬取得正则方法，得到大致内容
		strs = re.findall(pattern,Outstr)           #这里的findall返回的是一个列表
		for i in strs:
			FirstDeal = re.sub('<.*?>',"",i)		#处理刚才得到的字符串，并且作进一步处理 ，将<>内的内容全部删除
			SecondDeal = re.sub('\s+',"、",FirstDeal)    #将所有的空字符全部换成、符号，方便查看
			SecondDeal = SecondDeal.replace('&nbsp;',"") #做最后处理
			FileHandle.write(SecondDeal)				 #将处理完成字符串写入文件
			FileHandle.write('\n')						 #控制每条招聘信息换行

	def GoStart(self,FileHandle):
		for page in range(0,143):					#每页循环处理
			Outstr = self.getContent(page)			
			self.getStr(Outstr,FileHandle)
			#FileHandle.write('\n')


if __name__ == '__main__':
	BaseUrl = 'http://hr.tencent.com/position.php?tid=0&lid=0&keywords=&start='
	Lastlink = '0#a'
	FileHandle = open('JobinfoOfTencent.txt','w')
	txzp = TXZP(BaseUrl,Lastlink)					#实例化一个TXZP类
#	outstr = txzp.getContent(1)
#	txzp.getStr(outstr,FileHandle)
#	FileHandle.write(outstr)
	txzp.GoStart(FileHandle)						
	FileHandle.close()								#关闭文件