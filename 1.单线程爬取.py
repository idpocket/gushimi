import time

import requests
from lxml import etree
import os



import queue
import threading

'''
URL= 'https://www.gushimi.org/shiren/5.html'

'''

class GSM(object):
    def __init__(self,url):

        self.url=url
        self.path = './gsm/'
        if os.path.exists(self.path)==False:
            os.mkdir('./gsm')

        pass
    def findUrls(self):
        try:
            r = requests.get(self.url)
            r.encoding='utf-8'
            html = etree.HTML(r.text)
            urls = html.xpath('''//*[@id="layer-photos-demo"]/div[1]/div[9]/div[2]/ul/li/a[1]/@href''')
            print(html)
            return urls
        except:
            print(f'获取页面链接失败')

        pass

    #获取所有诗歌的url链接
    def getUrls(self):
        for urls in  self.findUrls():
            url = 'https://www.gushimi.org'+urls
            print(url)
            yield url


    def getContent(self,url):
        try:
            r = requests.get(url)
            r.encoding = 'utf-8'
            html = etree.HTML(r.text)
            title = html.xpath('''//*[@id="layer-photos-demo"]/div[5]/div[1]/h2/text()''')[0]
            contents = html.xpath('''/html/body/div[7]/div[1]/div[5]/div[2]/div[3]//text()''')
            print(title,contents)
            return title,contents
            pass
        except:
            print(f'获取文章失败')

        pass



        pass
    def download(self,title,contents):
        path = self.path+f'{title}.txt'
        # if os.path.exists(path)==False:


        with open(path,'w+')as f:
            f.writelines(title)
            f.writelines('\n')
            for content in contents:
                f.writelines(content)
        print(f'{title}下载成功')


        pass

    def run(self):

        for url  in self.getUrls():

            html = self.getContent(url)
            title =html[0]
            content =html[1]
            self.download(title,content)

        # url = 'https://www.gushimi.org/gushi/5562.html'
        # html = self.getContent(url)
        # title =html[0]
        # content =html[1]
        # self.download(title,content)



        pass
if __name__ == '__main__':
    url = 'https://www.gushimi.org/shiren/5.html'
    # content = 'https://www.gushimi.org/gushi/5342.html'
    gsm = GSM(url)
    st = time.time()
    gsm.run()
    et = time.time()
    print(f'总共用时：{et-st}')
