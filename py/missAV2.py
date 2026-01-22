# -*- coding: utf-8 -*-
from base.spider import Spider
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse, urlencode, parse_qs, unquote
import time
import json
import base64

class Spider(Spider):
    def __init__(self):
        super().__init__()
        
    def getName(self):
        return "MissAV2"
        
    def init(self, extend):
        self.base_url = "https://www.missav2.icu"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.missav2.icu/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def homeContent(self, filter):
        """首页分类和筛选"""
        categories = [
            {"type_id": "actresses", "type_name": "女优一览"},
            {"type_id": "actresses/ranking", "type_name": "女优排行"},
            {"type_id": "genres", "type_name": "类型"},
            {"type_id": "makers", "type_name": "发行商"},
        ]
        
        filter_options = [
            {"n": "所有", "v": ""},
            {"n": "单人作品", "v": "individual"},
            {"n": "多人作品", "v": "multiple"},
            {"n": "中文字幕", "v": "chinese-subtitle"},
        ]
        
        sort_options = [
            {"n": "默认", "v": ""},
            {"n": "发行日期", "v": "released_at"},
            {"n": "最近更新", "v": "published_at"},
            {"n": "收藏数", "v": "saved"},
            {"n": "今日浏览", "v": "today_views"},
            {"n": "本周浏览", "v": "weekly_views"},
            {"n": "本月浏览", "v": "monthly_views"},
            {"n": "总浏览", "v": "views"},
        ]
        
        actress_filters = [
            {
                "key": "sort",
                "name": "排序",
                "value": [
                    {"n": "影片数量", "v": "videos"},
                    {"n": "出道时间", "v": "debut"}
                ]
            },
            {
                "key": "height",
                "name": "身高",
                "value": [
                    {"n": "131-135cm", "v": "131-135"},
                    {"n": "136-140cm", "v": "136-140"},
                    {"n": "141-145cm", "v": "141-145"},
                    {"n": "146-150cm", "v": "146-150"},
                    {"n": "151-155cm", "v": "151-155"},
                    {"n": "156-160cm", "v": "156-160"},
                    {"n": "161-165cm", "v": "161-165"},
                    {"n": "166-170cm", "v": "166-170"},
                    {"n": "171-175cm", "v": "171-175"},
                    {"n": "176-180cm", "v": "176-180"},
                    {"n": "181-185cm", "v": "181-185"},
                    {"n": "186-190cm", "v": "186-190"}
                ]
            },
            {
                "key": "cup",
                "name": "罩杯",
                "value": [
                    {"n": "A", "v": "A"},
                    {"n": "B", "v": "B"},
                    {"n": "C", "v": "C"},
                    {"n": "D", "v": "D"},
                    {"n": "E", "v": "E"},
                    {"n": "F", "v": "F"},
                    {"n": "G", "v": "G"},
                    {"n": "H", "v": "H"}
                ]
            },
            {
                "key": "age",
                "name": "年龄",
                "value": [
                    {"n": "18-", "v": "18-"},
                    {"n": "20-", "v": "20-"},
                    {"n": "25-", "v": "25-"},
                    {"n": "30-", "v": "30-"},
                    {"n": "35-", "v": "35-"},
                    {"n": "40-", "v": "40-"},
                    {"n": "45-", "v": "45-"},
                    {"n": "50-", "v": "50-"},
                    {"n": "55-", "v": "55-"},
                    {"n": "60-", "v": "60"}
                ]
            },
            {
                "key": "debut",
                "name": "出道年份",
                "value": [
                    {"n": "1999", "v": "1999"},
                    {"n": "2000", "v": "2000"},
                    {"n": "2001", "v": "2001"},
                    {"n": "2002", "v": "2002"},
                    {"n": "2003", "v": "2003"},
                    {"n": "2004", "v": "2004"},
                    {"n": "2005", "v": "2005"},
                    {"n": "2006", "v": "2006"},
                    {"n": "2007", "v": "2007"},
                    {"n": "2008", "v": "2008"},
                    {"n": "2009", "v": "2009"},
                    {"n": "2010", "v": "2010"},
                    {"n": "2011", "v": "2011"},
                    {"n": "2012", "v": "2012"},
                    {"n": "2013", "v": "2013"},
                    {"n": "2014", "v": "2014"},
                    {"n": "2015", "v": "2015"},
                    {"n": "2016", "v": "2016"},
                    {"n": "2017", "v": "2017"},
                    {"n": "2018", "v": "2018"},
                    {"n": "2019", "v": "2019"},
                    {"n": "2020", "v": "2020"},
                    {"n": "2021", "v": "2021"},
                    {"n": "2022", "v": "2022"},
                    {"n": "2023", "v": "2023"},
                    {"n": "2024", "v": "2024"},
                    {"n": "2025", "v": "2025"}
                ]
            },
            {
                "key": "filters",
                "name": "视频过滤",
                "value": filter_options
            },
            {
                "key": "sort",
                "name": "视频排序",
                "value": sort_options
            }
        ]
        
        common_filters = [
            {
                "key": "filters",
                "name": "过滤",
                "value": filter_options
            },
            {
                "key": "sort",
                "name": "排序",
                "value": sort_options
            }
        ]
        
        filters = {}
        filters["actresses"] = actress_filters
        for category in ["actresses/ranking", "genres", "makers"]:
            filters[category] = common_filters
        
        return {
            "class": categories,
            "filters": filters
        }

    def homeVideoContent(self):
        """首页推荐视频"""
        try:
            url = f"{self.base_url}"
            print(f"首页URL: {url}")
            
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            html = response.text
            
            videos = self._parse_video_grid(html)
            
            return {
                'list': videos[:24]
            }
            
        except Exception as e:
            print(f"首页视频获取失败: {e}")
            return {'list': []}

    def categoryContent(self, tid, pg, filter, ext):
        """分类内容页"""
        try:
            print(f"原始分类参数: tid={tid}, pg={pg}, filter={filter}, ext={ext}")
            
            original_tid = tid
            if tid.startswith('http'):
                parsed_url = urlparse(tid)
                tid = parsed_url.path.lstrip('/')
                print(f"从URL中提取的tid: {tid}")
            
            try:
                tid = unquote(tid)
            except:
                pass
            
            print(f"处理后的tid: {tid}")
            
            if self._is_specific_category_page(tid, original_tid):
                print(f"具体分类页面（显示视频列表）: {tid}")
                return self._get_specific_category_videos(tid, pg, ext)
            else:
                print(f"分类列表页面: {tid}")
                return self._get_category_list(tid, pg, ext)
            
        except Exception as e:
            print(f"分类页面获取失败: {e}")
            import traceback
            traceback.print_exc()
            return {'list': []}
    
    def _is_specific_category_page(self, tid, original_tid=None):
        """判断是否是具体分类页面（显示视频列表）"""
        if original_tid and original_tid.startswith('http'):
            parsed_url = urlparse(original_tid)
            path = parsed_url.path.lstrip('/')
            tid = path
        
        try:
            tid = unquote(tid)
        except:
            pass
        
        patterns = [
            r'^dm\d+/actresses/.+$',
            r'^genres/.+$',
            r'^makers/.+$',
            r'^dm\d+/genres/.+$',
            r'^dm\d+/makers/.+$',
        ]
        
        for pattern in patterns:
            if re.match(pattern, tid):
                return True
        
        return False
    
    def _get_category_list(self, tid, pg, ext):
        """获取分类列表（女优/类型/发行商列表）"""
        try:
            try:
                tid = unquote(tid)
            except:
                pass
            
            url = f"{self.base_url}/{tid}"
            
            query_params = []
            
            if tid == "actresses":
                for key in ["sort", "height", "cup", "age", "debut"]:
                    if ext and key in ext and ext[key]:
                        query_params.append(f"{key}={ext[key]}")
            
            if ext and 'filters' in ext and ext['filters']:
                query_params.append(f"filters={ext['filters']}")
            
            if ext and 'sort' in ext and ext['sort']:
                query_params.append(f"sort={ext['sort']}")
            
            if pg != "1":
                query_params.append(f"page={pg}")
            
            if query_params:
                url = f"{url}?{'&'.join(query_params)}"
            
            print(f"分类列表URL: {url}")
            
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            html = response.text
            
            soup = BeautifulSoup(html, 'html.parser')
            
            if tid in ["actresses", "actresses/ranking"]:
                items = self._parse_actress_list(soup, tid)
            elif tid == "genres":
                items = self._parse_genre_list(soup, tid)
            elif tid == "makers":
                items = self._parse_maker_list(soup, tid)
            else:
                items = []
            
            print(f"解析到分类项数量: {len(items)}")
            
            pagecount = self._extract_page_count(soup)
            
            return {
                'list': items,
                'page': int(pg),
                'pagecount': pagecount or 9999,
                'limit': 24,
                'total': 999999
            }
            
        except Exception as e:
            print(f"获取分类列表失败: {e}")
            return {'list': []}
    
    def _get_specific_category_videos(self, tid, pg, ext):
        """获取具体分类的视频列表（如女优、类型、发行商）"""
        try:
            try:
                tid = unquote(tid)
            except:
                pass
            
            print(f"处理后的具体分类tid: {tid}")
            
            url = f"{self.base_url}/{tid}"
            
            query_params = []
            if ext and 'filters' in ext and ext['filters']:
                query_params.append(f"filters={ext['filters']}")
            if ext and 'sort' in ext and ext['sort']:
                query_params.append(f"sort={ext['sort']}")
            if pg != "1":
                query_params.append(f"page={pg}")
            if query_params:
                url = f"{url}?{'&'.join(query_params)}"
            
            print(f"具体分类视频列表URL: {url}")
            
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            html = response.text
            
            videos = self._parse_video_grid(html)
            
            print(f"解析到视频数量: {len(videos)}")
            
            soup = BeautifulSoup(html, 'html.parser')
            pagecount = self._extract_page_count(soup)
            
            return {
                'list': videos,
                'page': int(pg),
                'pagecount': pagecount or 9999,
                'limit': 24,
                'total': 999999
            }
            
        except Exception as e:
            print(f"获取具体分类视频失败: {e}")
            import traceback
            traceback.print_exc()
            return {'list': []}
    
    def _parse_video_grid(self, html):
        """解析视频网格 - 修复重复视频问题"""
        videos = []
        seen_ids = set()
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 查找所有可能的视频容器
            video_containers = []
            
            # 方法1: thumbnail group
            video_containers.extend(soup.find_all('div', class_='thumbnail group'))
            
            # 方法2: 网格中的项目
            grid = soup.find('div', class_='grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-5')
            if grid:
                grid_items = grid.find_all('div', recursive=False)
                for item in grid_items:
                    thumbnail_div = item.find('div', class_='thumbnail group')
                    if thumbnail_div:
                        video_containers.append(thumbnail_div)
            
            print(f"找到视频容器数量: {len(video_containers)}")
            
            for container in video_containers:
                video_data = self._parse_video_item(container)
                if video_data:
                    vod_id = video_data['vod_id']
                    
                    # 获取标准化的ID（去除uncensored-leak等后缀）
                    normalized_id = self._get_normalized_video_id(vod_id)
                    
                    if normalized_id not in seen_ids:
                        seen_ids.add(normalized_id)
                        videos.append(video_data)
                        print(f"添加视频: {video_data['vod_name']} (ID: {vod_id}, 标准化: {normalized_id})")
                    else:
                        print(f"跳过重复视频: {vod_id} (标准化: {normalized_id})")
            
            # 如果没有找到足够的视频，尝试备用方法
            if len(videos) < 5:
                print(f"视频数量少({len(videos)})，尝试备用方法...")
                all_links = soup.find_all('a', href=True)
                
                for link in all_links:
                    href = link.get('href', '')
                    if self._is_video_link(href):
                        vod_id = self._extract_video_id(href)
                        if vod_id:
                            normalized_id = self._get_normalized_video_id(vod_id)
                            
                            if normalized_id not in seen_ids:
                                seen_ids.add(normalized_id)
                                
                                title = ''
                                img = link.find('img')
                                if img:
                                    title = img.get('alt', '')
                                    cover = img.get('data-src') or img.get('src', '')
                                    cover = self._fix_url(cover) if cover else ''
                                else:
                                    title = link.get_text(strip=True)
                                    cover = ''
                                
                                if not title:
                                    title = vod_id.upper()
                                
                                video_info = {
                                    'vod_id': vod_id,
                                    'vod_name': title,
                                    'vod_pic': cover,
                                    'vod_remarks': vod_id.upper() or 'MissAV2',
                                    'vod_tag': 'video'
                                }
                                
                                videos.append(video_info)
                                print(f"从链接添加视频: {title} (ID: {vod_id}, 标准化: {normalized_id})")
            
            print(f"总共解析到视频数量（已去重）: {len(videos)}")
            return videos
            
        except Exception as e:
            print(f"解析视频网格失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_normalized_video_id(self, vod_id):
        """获取标准化的视频ID，去除uncensored-leak等后缀"""
        if not vod_id:
            return vod_id
        
        # 定义要去除的后缀模式
        suffix_patterns = [
            r'-uncensored-leak$',
            r'-leak$',
            r'-uncensored$',
            r'-censored$',
            r'-hd$',
            r'-full$',
            r'-complete$',
            r'-special$',
        ]
        
        normalized_id = vod_id.lower()
        
        # 去除常见后缀
        for pattern in suffix_patterns:
            if re.search(pattern, normalized_id):
                normalized_id = re.sub(pattern, '', normalized_id)
                break
        
        # 确保符合视频ID格式（字母-数字）
        match = re.match(r'^([a-z]+-\d+)', normalized_id)
        if match:
            return match.group(1)
        
        return vod_id
    
    def _parse_video_item(self, thumbnail_div):
        """解析单个视频项"""
        try:
            # 查找视频链接
            video_link = None
            links = thumbnail_div.find_all('a', href=True)
            
            for link in links:
                href = link.get('href', '')
                if self._is_video_link(href):
                    video_link = link
                    break
            
            if not video_link:
                if thumbnail_div.name == 'a':
                    href = thumbnail_div.get('href', '')
                    if self._is_video_link(href):
                        video_link = thumbnail_div
                else:
                    parent = thumbnail_div.parent
                    if parent and parent.name == 'a':
                        href = parent.get('href', '')
                        if self._is_video_link(href):
                            video_link = parent
            
            if not video_link:
                return None
            
            href = video_link.get('href', '')
            
            # 提取视频ID
            vod_id = self._extract_video_id(href)
            if not vod_id:
                return None
            
            # 提取标题
            title = ''
            title_div = thumbnail_div.find('div', class_='my-2 text-sm text-nord4 truncate')
            if title_div:
                title_a = title_div.find('a')
                if title_a:
                    title = title_a.get_text(strip=True)
                else:
                    title = title_div.get_text(strip=True)
            
            if not title:
                img = thumbnail_div.find('img')
                if img:
                    title = img.get('alt', '')
            
            if not title:
                title = video_link.get_text(strip=True)
            
            if not title:
                # 使用标准化的ID作为标题
                normalized_id = self._get_normalized_video_id(vod_id)
                title = normalized_id.upper()
            
            # 提取封面
            cover = ''
            img = thumbnail_div.find('img')
            if img:
                cover = img.get('data-src') or img.get('src', '')
                if cover:
                    cover = self._fix_url(cover)
            
            # 提取时长
            duration = ''
            duration_span = thumbnail_div.find('span', class_='absolute bottom-1 right-1')
            if duration_span:
                duration = duration_span.get_text(strip=True)
            else:
                duration_span = thumbnail_div.find('span', class_=re.compile(r'time|duration|length'))
                if duration_span:
                    duration = duration_span.get_text(strip=True)
            
            # 优先使用标准化的ID作为备注
            normalized_id = self._get_normalized_video_id(vod_id)
            remarks = normalized_id.upper()
            
            video_info = {
                'vod_id': vod_id,
                'vod_name': title,
                'vod_pic': cover or '',
                'vod_remarks': remarks or vod_id.upper() or 'MissAV2',
                'vod_tag': 'video'
            }
            
            return video_info
            
        except Exception as e:
            print(f"解析视频项失败: {e}")
            return None
    
    def _parse_actress_list(self, soup, tid):
        """解析女优列表"""
        items = []
        
        print("开始解析女优列表...")
        
        actress_grid = soup.find('ul', class_=re.compile(r'mx-auto grid grid-cols-2'))
        
        if not actress_grid:
            actress_items = soup.find_all('a', href=re.compile(r'/dm\d+/actresses/'))
            print(f"直接找到女优链接数量: {len(actress_items)}")
            
            for link in actress_items:
                try:
                    href = link.get('href', '')
                    if not href:
                        continue
                    
                    vod_id = href.lstrip('/')
                    
                    try:
                        vod_id = unquote(vod_id)
                    except:
                        pass
                    
                    cover = ''
                    img = link.find('img')
                    if img:
                        cover = img.get('src') or img.get('data-src', '')
                        if cover:
                            cover = self._fix_url(cover)
                    
                    name = link.get_text(strip=True)
                    if not name:
                        parts = vod_id.split('/')
                        if len(parts) >= 3:
                            name = parts[-1]
                        else:
                            name = '女优'
                    
                    item_info = {
                        'vod_id': vod_id,
                        'vod_name': name,
                        'vod_pic': cover,
                        'vod_remarks': '女优',
                        'vod_tag': 'folder'
                    }
                    
                    items.append(item_info)
                except Exception as e:
                    print(f"解析女优链接失败: {e}")
                    continue
            return items
        
        actress_items = actress_grid.find_all('li', recursive=False)
        print(f"在网格中找到女优项数量: {len(actress_items)}")
        
        for item in actress_items:
            try:
                link = item.find('a', href=re.compile(r'/dm\d+/actresses/'))
                if not link:
                    continue
                
                href = link.get('href', '')
                if not href:
                    continue
                
                vod_id = href.lstrip('/')
                
                try:
                    vod_id = unquote(vod_id)
                except:
                    pass
                
                cover = ''
                img = item.find('img')
                if img:
                    cover = img.get('src') or img.get('data-src', '')
                    if cover:
                        cover = self._fix_url(cover)
                
                name = ''
                h4 = item.find('h4')
                if h4:
                    name = h4.get_text(strip=True)
                
                if not name:
                    name = link.get_text(strip=True)
                
                if not name:
                    parts = vod_id.split('/')
                    if len(parts) >= 3:
                        name = parts[-1]
                    else:
                        name = '女优'
                
                video_count = ''
                debut_year = ''
                
                p_tags = item.find_all('p')
                for p in p_tags:
                    text = p.get_text(strip=True)
                    if '條影片' in text or '件作品' in text:
                        video_count = text
                    elif '出道' in text:
                        debut_year = text
                    elif text.isdigit() and len(text) == 4:
                        debut_year = f"{text} 出道"
                
                remarks = []
                if video_count:
                    remarks.append(video_count)
                if debut_year:
                    remarks.append(debut_year)
                
                item_info = {
                    'vod_id': vod_id,
                    'vod_name': name or '女优',
                    'vod_pic': cover,
                    'vod_remarks': ' | '.join(remarks) if remarks else '女优',
                    'vod_tag': 'folder'
                }
                
                items.append(item_info)
                
            except Exception as e:
                print(f"解析女优项目失败: {e}")
                continue
        
        print(f"总共解析到女优数量: {len(items)}")
        return items
    
    def _parse_genre_list(self, soup, tid):
        """解析类型列表"""
        items = []
        
        grid = soup.find('div', class_='grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4')
        if not grid:
            grid = soup.find('div', class_='grid')
        
        if not grid:
            genre_links = soup.find_all('a', href=re.compile(r'/dm\d+/genres/'))
            print(f"直接找到类型链接数量: {len(genre_links)}")
            
            for link in genre_links:
                try:
                    href = link.get('href', '')
                    if not href:
                        continue
                    
                    vod_id = href.lstrip('/')
                    
                    try:
                        vod_id = unquote(vod_id)
                    except:
                        pass
                    
                    name = link.get_text(strip=True)
                    
                    item_info = {
                        'vod_id': vod_id,
                        'vod_name': name or '类型',
                        'vod_pic': '',
                        'vod_remarks': '类型',
                        'vod_tag': 'folder'
                    }
                    
                    items.append(item_info)
                except:
                    continue
            return items
        
        grid_items = grid.find_all('div', recursive=False)
        
        for item in grid_items:
            try:
                link = item.find('a', href=re.compile(r'/dm\d+/genres/'))
                if not link:
                    continue
                
                href = link.get('href', '')
                if not href:
                    continue
                
                vod_id = href.lstrip('/')
                
                try:
                    vod_id = unquote(vod_id)
                except:
                    pass
                
                name = link.get_text(strip=True)
                
                video_count = ''
                p_tags = item.find_all('p')
                for p in p_tags:
                    text = p.get_text(strip=True)
                    if '條影片' in text or '件作品' in text:
                        video_count = text
                        break
                
                item_info = {
                    'vod_id': vod_id,
                    'vod_name': name or '类型',
                    'vod_pic': '',
                    'vod_remarks': video_count or '类型',
                    'vod_tag': 'folder'
                }
                
                items.append(item_info)
                
            except Exception as e:
                print(f"解析类型项目失败: {e}")
                continue
        
        return items
    
    def _parse_maker_list(self, soup, tid):
        """解析发行商列表"""
        items = []
        
        grid = soup.find('div', class_='grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4')
        if not grid:
            grid = soup.find('div', class_='grid')
        
        if not grid:
            maker_links = soup.find_all('a', href=re.compile(r'/dm\d+/makers/'))
            print(f"直接找到发行商链接数量: {len(maker_links)}")
            
            for link in maker_links:
                try:
                    href = link.get('href', '')
                    if not href:
                        continue
                    
                    vod_id = href.lstrip('/')
                    
                    try:
                        vod_id = unquote(vod_id)
                    except:
                        pass
                    
                    name = link.get_text(strip=True)
                    
                    item_info = {
                        'vod_id': vod_id,
                        'vod_name': name or '发行商',
                        'vod_pic': '',
                        'vod_remarks': '发行商',
                        'vod_tag': 'folder'
                    }
                    
                    items.append(item_info)
                except:
                    continue
            return items
        
        grid_items = grid.find_all('div', recursive=False)
        
        for item in grid_items:
            try:
                link = item.find('a', href=re.compile(r'/dm\d+/makers/'))
                if not link:
                    continue
                
                href = link.get('href', '')
                if not href:
                    continue
                
                vod_id = href.lstrip('/')
                
                try:
                    vod_id = unquote(vod_id)
                except:
                    pass
                
                name = link.get_text(strip=True)
                
                video_count = ''
                p_tags = item.find_all('p')
                for p in p_tags:
                    text = p.get_text(strip=True)
                    if '條影片' in text or '件作品' in text:
                        video_count = text
                        break
                
                item_info = {
                    'vod_id': vod_id,
                    'vod_name': name or '发行商',
                    'vod_pic': '',
                    'vod_remarks': video_count or '发行商',
                    'vod_tag': 'folder'
                }
                
                items.append(item_info)
                
            except Exception as e:
                print(f"解析发行商项目失败: {e}")
                continue
        
        return items
    
    def _is_video_link(self, href):
        """检查是否是视频链接"""
        if not href:
            return False
        
        exclude_keywords = ['/actresses/', '/genres/', '/makers/', '/search/', '/ranking', '?page=', '#', 'javascript:']
        if any(keyword in href for keyword in exclude_keywords):
            return False
        
        video_pattern = r'[a-zA-Z]+-\d+'
        
        if '/' in href:
            last_part = href.rstrip('/').split('/')[-1]
            return bool(re.match(video_pattern, last_part))
        
        return bool(re.match(video_pattern, href))
    
    def _extract_video_id(self, href):
        """从链接中提取视频ID"""
        if not href:
            return ''
        
        if '/' in href:
            last_part = href.rstrip('/').split('/')[-1]
            if re.match(r'[a-zA-Z]+-\d+', last_part):
                return last_part
        
        if re.match(r'[a-zA-Z]+-\d+', href):
            return href
        
        return ''
    
    def _fix_url(self, url):
        """修复URL"""
        if not url:
            return ''
        
        if url.startswith('//'):
            return 'https:' + url
        elif url.startswith('/'):
            return self.base_url + url
        elif not url.startswith('http'):
            return f"{self.base_url}/{url}"
        
        return url
    
    def _extract_page_count(self, soup):
        """提取页数"""
        try:
            pagination = soup.find('nav', class_=re.compile(r'flex items-center'))
            if pagination:
                links = pagination.find_all('a')
                max_page = 1
                for link in links:
                    href = link.get('href', '')
                    if 'page=' in href:
                        match = re.search(r'page=(\d+)', href)
                        if match:
                            page_num = int(match.group(1))
                            if page_num > max_page:
                                max_page = page_num
                return max_page if max_page > 1 else 1
            
            return 1
            
        except:
            return 1

    def detailContent(self, ids):
        """详情页 - 只处理视频详情"""
        vod_id = ids[0]
        
        print(f"详情页请求: vod_id={vod_id}")
        
        if not self._is_video_detail_page(vod_id):
            print(f"不是视频详情页，返回空列表: {vod_id}")
            return {'list': []}
        
        return self._get_video_detail(vod_id)
    
    def _is_video_detail_page(self, vod_id):
        """判断是否是视频详情页"""
        video_pattern = r'^[a-zA-Z]+-\d+'
        return bool(re.match(video_pattern, vod_id))
    
    def _get_video_detail(self, video_id):
        """获取视频详情"""
        try:
            # 使用标准化的视频ID访问详情页
            normalized_id = self._get_normalized_video_id(video_id)
            url = f"{self.base_url}/{normalized_id}"
            print(f"视频详情页URL: {url} (原始ID: {video_id}, 标准化: {normalized_id})")
            
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            html = response.text
            
            soup = BeautifulSoup(html, 'html.parser')
            
            detail_info = self._extract_video_detail(soup, normalized_id)
            
            return {
                'list': [detail_info]
            }
            
        except Exception as e:
            print(f"获取视频详情失败: {e}")
            # 如果使用标准化ID失败，尝试使用原始ID
            try:
                url = f"{self.base_url}/{video_id}"
                print(f"尝试使用原始ID: {url}")
                
                response = self.session.get(url, timeout=15)
                response.encoding = 'utf-8'
                html = response.text
                
                soup = BeautifulSoup(html, 'html.parser')
                
                detail_info = self._extract_video_detail(soup, video_id)
                
                return {
                    'list': [detail_info]
                }
            except:
                return {'list': []}
    
    def _extract_video_detail(self, soup, video_id):
        """从页面提取视频详细信息"""
        try:
            title = ""
            h1_tag = soup.find('h1', class_=re.compile(r'text-2xl|text-3xl|text-4xl'))
            if not h1_tag:
                h1_tag = soup.find('title')
            
            if h1_tag:
                title = h1_tag.get_text(strip=True)
                if ' - ' in title:
                    title = title.split(' - ')[0]
            
            cover = ""
            img = soup.find('img', class_=re.compile(r'object-cover|w-full|rounded-lg'))
            if not img:
                img = soup.find('img', alt=re.compile(title))
            
            if img:
                cover = self._fix_url(img.get('src', ''))
            
            tags = []
            tag_elements = soup.find_all('a', href=re.compile(r'/dm\d+/genres/|/series/'))
            for tag in tag_elements:
                tag_text = tag.get_text(strip=True)
                if tag_text and tag_text not in tags:
                    tags.append(tag_text)
            
            actors = []
            actor_elements = soup.find_all('a', href=re.compile(r'/dm\d+/actresses/'))
            for actor in actor_elements:
                actor_text = actor.get_text(strip=True)
                if actor_text and actor_text not in actors:
                    actors.append(actor_text)
            
            maker = ""
            maker_element = soup.find('a', href=re.compile(r'/dm\d+/makers/'))
            if maker_element:
                maker = maker_element.get_text(strip=True)
            
            duration = ""
            duration_element = soup.find('span', class_=re.compile(r'duration|time|length|text-sm'))
            if duration_element:
                duration = duration_element.get_text(strip=True)
            
            pub_date = ""
            date_elements = soup.find_all('p', class_=re.compile(r'text-sm'))
            for elem in date_elements:
                text = elem.get_text(strip=True)
                if '發行日期' in text or '配信開始日' in text or '発売日' in text:
                    pub_date = text.replace('發行日期：', '').replace('配信開始日：', '').replace('発売日：', '')
                    break
            
            code = video_id.upper() if video_id else ""
            
            description = []
            if actors:
                description.append(f"演员: {' | '.join(actors)}")
            if tags:
                description.append(f"类型: {' | '.join(tags)}")
            if maker:
                description.append(f"发行商: {maker}")
            if code:
                description.append(f"番号: {code}")
            if duration:
                description.append(f"时长: {duration}")
            if pub_date:
                description.append(f"发行日期: {pub_date}")
            
            return {
                'vod_id': video_id,
                'vod_name': title or video_id,
                'vod_pic': cover,
                'type_name': ' | '.join(tags[:3]) if tags else '日本AV',
                'vod_year': pub_date[:4] if pub_date and len(pub_date) >= 4 else '',
                'vod_area': '日本',
                'vod_remarks': duration or code or 'MissAV2',
                'vod_actor': ' | '.join(actors[:5]) if actors else '',
                'vod_director': maker or '',
                'vod_content': ' | '.join(description) if description else '日本AV作品',
                'vod_play_from': '默认播放',
                'vod_play_url': f'正片${video_id}'
            }
            
        except Exception as e:
            print(f"提取视频详情失败: {e}")
            return {
                'vod_id': video_id,
                'vod_name': video_id,
                'vod_pic': '',
                'vod_play_from': '默认播放',
                'vod_play_url': f'正片${video_id}'
            }

    def searchContent(self, key, quick, pg="1"):
        """搜索功能"""
        try:
            encoded_key = quote(key)
            url = f"{self.base_url}/search/{encoded_key}"
            if pg != "1":
                url = f"{url}?page={pg}"
            
            print(f"搜索URL: {url}")
            
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            html = response.text
            
            videos = self._parse_video_grid(html)
            
            print(f"搜索到视频数量: {len(videos)}")
            
            return {
                'list': videos,
                'page': int(pg),
                'pagecount': 9999,
                'limit': 30,
                'total': 999999
            }
            
        except Exception as e:
            print(f"搜索失败: {e}")
            import traceback
            traceback.print_exc()
            return {'list': []}

    def playerContent(self, flag, id, vipFlags):
        """播放页"""
        try:
            print(f"播放请求: flag={flag}, id={id}")
            
            if '$' in id:
                parts = id.split('$')
                vod_id = parts[1] if len(parts) > 1 else id
            else:
                vod_id = id
            
            print(f"解析后的视频ID: {vod_id}")
            
            if any(keyword in vod_id for keyword in ['/actresses/', '/genres/', '/makers/']):
                print(f"分类页面不处理播放: {vod_id}")
                return {
                    'parse': 0,
                    'url': '',
                    'header': ''
                }
            
            # 使用标准化的视频ID访问播放页
            normalized_id = self._get_normalized_video_id(vod_id)
            play_url = f"{self.base_url}/{unquote(normalized_id)}"
            print(f"播放页URL: {play_url} (原始: {vod_id}, 标准化: {normalized_id})")
            
            return {
                'parse': 1,
                'url': play_url,
                'header': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': f'{self.base_url}/',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
            }
            
        except Exception as e:
            print(f"播放页处理失败: {e}")
            import traceback
            traceback.print_exc()
            return {
                'parse': 1,
                'url': f"{self.base_url}",
                'header': self.session.headers
            }

    def isVideoFormat(self, url):
        """检查是否是视频格式"""
        if any(keyword in url for keyword in ['/actresses/', '/genres/', '/makers/']):
            return False
        if re.match(r'[a-zA-Z]+-\d+', url):
            return True
        return False

    def manualVideoCheck(self):
        return False

    def destroy(self):
        if hasattr(self, 'session'):
            self.session.close()

    def localProxy(self, param):
        return []