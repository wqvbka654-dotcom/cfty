# -*- coding: utf-8 -*-
# by @嗷呜
import gzip
import html
import json
import re
import sys
import base64
from base64 import b64decode
from urllib.parse import unquote, urlparse
import requests
from pyquery import PyQuery as pq
sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def init(self, extend='{}'):
        config = json.loads(extend)
        self.proxies = config.get('proxy', {})
        self.plp = config.get('plp', '')
        pass

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    host = 'https://javxx.com'

    contr = 'cn'

    conh = f'{host}/{contr}'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'referer': f'{conh}/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    gcate = 'H4sIAAAAAAAAA6tWejan4dm0DUpWCkp5qeVKOkrPm9e+nL4CxM/ILwHygfIv9k8E8YtSk1PzwELTFzxf0AgSKs0DChXnF6WmwIWfbW55OWcTqqRuTmpiNljN8427n3asBsmmp+YVpRaDtO2Z8nTiDJBQYnIJUKgYLPq0Y9uTvXOeTm0DSeQCdReBRJ9vBmqfDhIqTi3KhGhf0P587T6QUElierFSLQCk4MAf0gAAAA=='

    flts = 'H4sIAAAAAAAAA23QwYrCMBAG4FeRnH0CX0WKBDJiMRpoY0WkIOtFXLQU1IoEFFHWw4qHPazgii/TRPctNKK1Ro/zz8cM/PkmKkMD5TLIZQ5HWVTFFUiNHqY1PeebyNOxAxSwCwWCOWitMxmEcttW0VKJKfKzN4kJAfLk1O9OdmemKzF+B8f2+j9aPVacEdwoeDbU3TuJd93LgdPXx1F8PmAdoEwNqTaBDFemrLAqL72hSnReqcuvDkgCRUsGkfqenw59AxaxxxybP9uRuFjkW5reai7alIOTKjoJzKoxpUnDvWG8bcnlj/obyHCcKi95JxeTeN9LEcu3zoYr9GndAQAA'

    actft = 'H4sIAAAAAAAAA22UTUsbURSG/0qYtQMxZvIhIvidxI/oVpEy6GiCmpFkEhEpVBcqikYprV2kG6GkhYK2XRbxzziT+C88c2/OnLnnunznec47zJ3LWTsydpxDYzRhVJzqdsUzhoyavecoD1r2bjN8snZktEIwPJI0h0fSoRqL/vW33p9/xsehyLLgcZ4sETUrDcNp6pJRt2A4TV0yapYFwxZ1yahbMGxRl4yalYHhDHXJqFswnKEuGTUrC8NZ6pJRt2A4S10yalYOhnPUJaNuwXCOumTUrDwM56lLRrTWQ29wNzaa+7GLIRO/FRPYM9F7+hV8f6D3TCKZ5GQKyRQn00imOZlBMsPJLJJZTuaQzHFSQFLgpIikyEkJSYmTeSTznCwgWeBkEckiJ0tIljgpIylzsoxkmZMVJCucrCJZRRL/9/a2E/v3MvF/H14cLBlLpJL+32OqTyXNVHTJRFCxZaaiYREUDMuFVo0IKrZM2jEiKBjWCS0XEVRsmbRVRFAwLBBaJyIoGHZCPpoeT2TkZ8fPruHW4xt1EPnpCTyo8buf/ZsreseG26x5CPvd09f72+DL4+tZmxTP3bQPP7SqzkEDxZf/F8Hdj373pNe5JPHAcXZ2mRk8tP3bn9zcc2te5R016JzrasMTnrMZiZ1Pfvsu+H3ff75m4pbdcutVT3W/dsAND279DSxD8pmOBgAA'

    def homeContent(self, filter):
        data = self.getpq(requests.get(f"{self.conh}", headers=self.headers, proxies=self.proxies).text)
        result = {}
        cate = self.ungzip(self.gcate)
        classes = []
        filters = {}
        for k, j in cate.items():
            classes.append({
                'type_name': k,
                'type_id': j
            })
            if j == 'actresses':
                fts = self.ungzip(self.actft)
            else:
                fts = self.ungzip(self.flts)
            filters[j] = fts
        result['class'] = classes
        result['filters'] = filters
        result['list'] = self.getvl(data('.vid-items .item'))
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        videos = []
        if tid in ['genres', 'makers', 'series', 'tags']:
            gggg = tid if tid == 'series' else tid[:-1]
            pagecount = 1
            data = self.getpq(requests.get(f"{self.conh}/{tid}", headers=self.headers, proxies=self.proxies).text)
            for i in data(f'.term-items.{gggg} .item').items():
                videos.append({
                    'vod_id': i('a').attr('href'),
                    'vod_name': i('h2').text(),
                    'vod_remarks': i('.meta').text(),
                    'vod_tag': 'folder',
                    'style': {"type": "rect", "ratio": 2}
                })
        elif tid == 'actresses':
            params = {
                'height': extend.get('height'),
                "cup": extend.get('cup'),
                "sort": extend.get('sort'),
                'age': extend.get('age'),
                "page": pg
            }
            c_params = {k: v for k, v in params.items() if v}
            data = self.getpq(
                requests.get(f"{self.conh}/{tid}", headers=self.headers, params=c_params, proxies=self.proxies).text)
            pagecount = self.getpgc(data('ul.pagination li').eq(-1))
            for i in data('.chanel-items .item').items():
                i = i('.main')
                videos.append({
                    'vod_id': i('.info a').attr('href'),
                    'vod_name': i('.info h2').text(),
                    'vod_pic': i('.avatar img').attr('src'),
                    'vod_year': i('.meta div div').eq(-1).text(),
                    'vod_remarks': i('.meta div div').eq(0).text(),
                    'vod_tag': 'folder',
                    'style': {"type": "oval", "ratio": 0.75}
                })
        else:
            tid = tid.split('_click')[0].replace(f"/{self.contr}/", "")
            params = {
                "filter": extend.get('filter'),
                "sort": extend.get('sort'),
                "page": pg
            }
            c_params = {k: v for k, v in params.items() if v}
            data = self.getpq(
                requests.get(f"{self.conh}/{tid}", params=c_params, headers=self.headers, proxies=self.proxies).text)
            videos = self.getvl(data('.vid-items .item'))
            pagecount = self.getpgc(data('ul.pagination li').eq(-1))
        result = {}
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = pagecount
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        data = self.getpq(requests.get(f"{self.host}{ids[0]}", headers=self.headers, proxies=self.proxies).text)
        dv = data('#video-details')
        detail_url = f"{self.host}{ids[0]}"  # 当前详情页URL，用于嗅探
        pnpn = {
            '老僧酿酒、名妓读经': f"{data('#video-info h1').text()}${detail_url}",  # 主视频直接用详情页URL
            '书生玩剑': '#'.join(
                [f"{i('.info .title span').eq(-1).text()}${self.host + i('.info .title').attr('href')}" for i in
                 data('.main .vid-items .item').items()]),
            '将军作文': '#'.join([f"{i('.info .title span').eq(-1).text()}${self.host + i('.info .title').attr('href')}" for i in
                              data('.vid-items.side .item').items()])
        }
        n, p = [], []
        for k, v in pnpn.items():
            if v:
                n.append(k)
                p.append(v)
        # 过滤vod_content中的广告/弹窗关键词和脚本
        content = dv('.content').text()
        content = re.sub(r'(广告|弹窗|popup|alert|ad|script)', '', content, flags=re.IGNORECASE)
        content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        vod = {
            'vod_content': content.strip(),
            'vod_play_from': '$$$'.join(n),
            'vod_play_url': '$$$'.join(p)
        }
        a, b, c, d = [], [], [], []
        for i in dv('.meta div').items():
            if re.search(r'发布日期', i('label').text()):
                vod['vod_year'] = i('span').text()
            elif re.search(r'演员', i('label').text()):
                a.extend(['[a=cr:' + json.dumps(
                    {'id': f"{j.attr('href')}_click", 'name': j.text()}) + '/]' + j.text() + '[/a]' for j in
                          i('a').items()])
            elif re.search(r'制作商|系列', i('label').text()):
                b.extend(['[a=cr:' + json.dumps(
                    {'id': f"{j.attr('href')}_click", 'name': j.text()}) + '/]' + j.text() + '[/a]' for j in
                          i('a').items()])
            elif re.search(r'标签', i('label').text()):
                c.extend(['[a=cr:' + json.dumps(
                    {'id': f"{j.attr('href')}_click", 'name': j.text()}) + '/]' + j.text() + '[/a]' for j in
                          i('a').items()])
            elif re.search(r'类别', i('label').text()):
                d.extend(['[a=cr:' + json.dumps(
                    {'id': f"{j.attr('href')}_click", 'name': j.text()}) + '/]' + j.text() + '[/a]' for j in
                          i('a').items()])
        vod.update({'vod_actor': ' '.join(a), 'vod_director': ' '.join(b), 'vod_remarks': ' '.join(c),
                    'vod_content': ' '.join(d) + '\n' + vod['vod_content']})
        return {'list': [vod]}

    def searchContent(self, key, quick, pg="1"):
        params = {'keyword': key, 'page': pg}
        data = self.getpq(
            requests.get(f"{self.conh}/search", headers=self.headers, params=params, proxies=self.proxies).text)
        return {'list': self.getvl(data('.vid-items .item')), 'page': pg}

    def playerContent(self, flag, id, vipFlags):
        # 直接使用详情页URL进行嗅探，无需解密
        if id.startswith('http'):  # 已完整URL
            url = id
        else:
            # 对于子视频或主视频，确保是完整URL
            if not id.startswith('/'):
                # 如果是相对路径，补全（但通常已经是完整href）
                pass
            url = f"{self.host}{id}" if not id.startswith('http') else id
        
        # 构建反弹窗请求头
        headers = {
            'user-agent': self.headers['user-agent'], 
            'origin': self.host, 
            'referer': f"{self.host}/",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'dnt': '1',  # Do Not Track，减少跟踪弹窗
        }
        return {'parse': 1, 'url': url, 'header': headers}

    def localProxy(self, param):
        pass

    def liveContent(self, url):
        pass

    def getvl(self, data):
        videos = []
        for i in data.items():
            img = i('.img')
            imgurl = img('.image img').attr('src')
            if imgurl:
                imgurl = imgurl.replace("/s360/", "/s1080/")
            videos.append({
                'vod_id': img('a').attr('href'),
                'vod_name': i('.info .title').text(),
                'vod_pic': imgurl,
                'vod_year': i('.info .meta div').eq(-1).text(),
                'vod_remarks': i('.duration').text(),
                'style': {"type": "rect", "ratio": 1.33}
            })
        return videos

    def getpgc(self, data):
        try:
            if data:
                if data('a'):
                    return int(data('a').attr('href').split('page=')[-1])
                else:
                    return int(data.text())
            else:
                raise Exception("获取页数失败")
        except:
            return 1

    def p_qjs(self, js_code):
        try:
            from com.whl.quickjs.wrapper import QuickJSContext
            ctx = QuickJSContext.create()
            jctx = ctx.evaluate(js_code)
            code = jctx.strip().split('const posterUrl', 1)[0].split('{', 1)[-1]
            result = ctx.evaluate(f"{code}\nJSON.stringify(media)")
            ctx.destroy()
            return json.loads(result)

        except Exception as e:
            self.log(f"执行失败: {e}")
            return []

    def ungzip(self, data):
        result = gzip.decompress(b64decode(data)).decode()
        return json.loads(result)

    def getpq(self, data):
        try:
            return pq(data)
        except Exception as e:
            print(f"{str(e)}")
            return pq(data.encode('utf-8'))
