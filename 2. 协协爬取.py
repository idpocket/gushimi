import asyncio
import time

import aiohttp,aiofiles
import requests
from lxml import etree




async def save(url):

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await  resp.text()
                html = etree.HTML(html)
                title = html.xpath('''//*[@id="layer-photos-demo"]/div[5]/div[1]/h2/text()''')[0]
                contents = html.xpath('''/html/body/div[7]/div[1]/div[5]/div[2]/div[3]//text()''')
                path = './wqsc/'+f'{title}.txt'


                async with aiofiles.open(path,'w')as f:

                    await f.write(f'{title}\n')
                    await f.writelines(contents)
                    # for content in contents:
                    #     await f.writelines(content)
                    print(f'{title}下载成功')




                # print(title,contents,path)
    except:
        print(f'{url}:下载失败')

async def findUrls(url):
    try:

        r = requests.get(url)
        r.encoding = 'utf-8'
        html = etree.HTML(r.text)
        urls = html.xpath('''//*[@id="layer-photos-demo"]/div[1]/div[9]/div[2]/ul/li/a[1]/@href''')#列表
        tasks = []

        urls =  [f'https://www.gushimi.org{url}' for url in urls]
        #准备异步爬虫
        for url in urls:
            tasks.append(asyncio.create_task(save(url)))

        # await asyncio.wait(tasks)
        await asyncio.wait(tasks)


        print(urls)
        # return urls
    except:
        print(f'获取页面链接失败')
if __name__ == '__main__':
    url = 'https://www.gushimi.org/shiren/5.html'
    st = time.time()
    asyncio.run( findUrls(url))
    et = time.time()
    print(f'总共用时：{et - st}')
