# coding=utf-8
# !/usr/bin/python
# by嗷呜
import json
import sys
import requests
from bs4 import BeautifulSoup
import re
from base64 import b64decode, b64encode
from pyquery import PyQuery as pq
from requests import Session

sys.path.append('..')
from base.spider import Spider

xurl = "https://www.fullhd.xxx/"

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
}

class Spider(Spider):

    def init(self, extend=""):
        pass

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-full-version': '"133.0.6943.98"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-full-version-list': '"Not(A:Brand";v="99.0.0.0", "Google Chrome";v="133.0.6943.98", "Chromium";v="133.0.6943.98"',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'priority': 'u=0, i'
    }

    host = "https://www.fullhd.xxx"
    
    

    def homeContent(self, filter):
        result = {}
        cateManual = {
            "最新视频": "/latest-updates",
            "最佳视频": "/top-rated",
            "热门影片": "/most-popular"
        }
        classes = []
        filters = {}
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
        result['class'] = classes
        result['filters'] = filters
        return result

    def homeVideoContent(self):
        data = self.getpq()
        return {'list': self.getlist(data(".margin-fix .item"))}

    def categoryContent(self, cid, pg, filter, extend):
        result = {}
        if pg:
            page = int(pg)
        else:
            page = 1
        page = int(pg)
        videos = []

        if page == '1':
            url = f'{xurl}/{cid}/'

        else:
            url = f'{xurl}/{cid}/{str(page)}/'

        try:
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            doc = BeautifulSoup(res, "lxml")

            soups = doc.find_all('div', class_="margin-fix")

            for soup in soups:
                vods = soup.find_all('div', class_="item")

                for vod in vods:

                    names = vod.find_all('a')
                    name = names[0]['title']

                    ids = vod.find_all('a')
                    id = ids[0]['href']

                    pics = vod.find('img', class_="lazyload")
                    pic = pics['data-src']

                    if 'http' not in pic:
                        pic = xurl + pic

                    remarks = vod.find('div', class_="img thumb__img")
                    remark = remarks.text.strip()

                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": remark
                    }
                    videos.append(video)

        except:
            pass
        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        did = ids[0]
        result = {}
        videos = []
        playurl = ''
        if 'http' not in did:
            did = xurl + did
        res1 = requests.get(url=did, headers=headerx)
        res1.encoding = "utf-8"
        res = res1.text

        content = '资源来源于网络🚓侵权请联系删除👉' + self.extract_middle_text(res, '<h1>', '</h1>', 0)

        yanuan = self.extract_middle_text(res, '<span>Pornstars:</span>', '</div>', 1, 'href=".*?">(.*?)</a>')

        bofang = did

        videos.append({
            "vod_id": did,
            "vod_actor": yanuan,
            "vod_director": '',
            "vod_content": content,
            "vod_play_from": '💗数逼毛💗',
            "vod_play_url": bofang
        })

        result['list'] = videos
        return result

    def searchContent(self, key, quick, pg="1"):
        pass

    def playerContent(self, flag, id, vipFlags):
        headerx = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
        }
        parts = id.split("http")
        xiutan = 0
        if xiutan == 0:
            if len(parts) > 1:
                before_https, after_https = parts[0], 'http' + parts[1]
            res = requests.get(url=after_https, headers=headerx)
            res = res.text

            url2 = self.extract_middle_text(res, '<video', '</video>', 0).replace('\\', '')
            soup = BeautifulSoup(url2, 'html.parser')
            first_source = soup.find('source')
            src_value = first_source.get('src')

            response = requests.head(src_value, allow_redirects=False)
            if response.status_code == 302:
                redirect_url = response.headers['Location']

            response = requests.head(redirect_url, allow_redirects=False)
            if response.status_code == 302:
                redirect_url = response.headers['Location']

            result = {}
            result["parse"] = xiutan
            result["playUrl"] = ''
            result["url"] = redirect_url
            result["header"] = headerx
            return result

    def localProxy(self, param):
        pass

    # def gethost(self):
    #     try:
    #         response = self.fetch(f'{self.proxy}https://www.fullhd.xxx', headers=self.headers, allow_redirects=False)
    #         return response.headers['Location']
    #     except Exception as e:
    #         print(f"获取主页失败: {str(e)}")
    #         return "https://www.fullhd.xxx"

    # def e64(self, text):
    #     try:
    #         text_bytes = text.encode('utf-8')
    #         encoded_bytes = b64encode(text_bytes)
    #         return encoded_bytes.decode('utf-8')
    #     except Exception as e:
    #         print(f"Base64编码错误: {str(e)}")
    #         return ""

    # def d64(self, encoded_text):
    #     try:
    #         encoded_bytes = encoded_text.encode('utf-8')
    #         decoded_bytes = b64decode(encoded_bytes)
    #         return decoded_bytes.decode('utf-8')
    #     except Exception as e:
    #         print(f"Base64解码错误: {str(e)}")
    #         return ""

    def getlist(self, data):
        vlist = []

        for i in data.items():
            # 1. 尝试获取 img 元素
            img_element = i('img')

            # 2. 初始化 URL 为 None
            final_pic_url = None

            if img_element:
                # 3. 获取 src 和 data-src 属性
                src_value = img_element.attr('src')
                data_src_value = img_element.attr('data-src')

                # 4. 核心判断逻辑
                # 判断 src 是否存在 AND 是否以 Base64 占位符 'data:image/' 开头
                if src_value and src_value.startswith('data:image/'):
                    # 如果是占位符，使用 data-src 的值
                    final_pic_url = data_src_value
                else:
                    # 否则，使用 src 的值 (即使是 None 也没关系)
                    final_pic_url = src_value

            vlist.append({
                'vod_id': i('a').attr('href'),
                'vod_name': i('a').attr('title'),
                # 5. 使用经过判断处理的 URL
                'vod_pic': final_pic_url,
                'vod_remarks': i('.duration').text(),
                'style': {'ratio': 1.33, 'type': 'rect'}
            })

        return vlist

    def getpq(self, path=''):
        url = f"{self.host}{path}"
        data = self.fetch(url, headers=self.headers).text
        try:
            return pq(data)
        except Exception as e:
            print(f"{str(e)}")
            return pq(data.encode('utf-8'))

    # def getjsdata(self, data):
    #     vhtml = data("script[type='application/ld+json']").text()
    #     jst = json.loads(vhtml.split('initials=')[-1][:-1])
    #     return jst
