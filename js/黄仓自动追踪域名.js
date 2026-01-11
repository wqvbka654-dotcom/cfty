var rule = {
author: '黑可乐',
title: '绿色仓库',
类型: '影视',
host: '',
hostJs: $js.toString(() => {
    HOST = base64Decode('aHR0cDovL2hzY2submV0');
    let strU = fetch(HOST).match(/strU="(.*?)"/)[1];
    let locationU = strU + HOST + '/&p=/';
    let resp = fetch(locationU, {withHeaders: true, redirect: false});
    HOST = JSON.parse(resp).location
}),
headers: {'User-Agent': MOBILE_UA},
编码: 'utf-8',
timeout: 5000,

homeUrl: '/',
url: '/vodtype/fyfilter-fypage.html',
filter_url: '{{fl.cateId}}',
searchUrl: '/vodsearch/**----------fypage---.html',
detailUrl: '',

limit: 9,
double: false,
class_name: '',
class_url: '1&2&3&4',
filter_def: {
1: {cateId: '1'},
2: {cateId: '2'},
3: {cateId: '3'},
4: {cateId: '4'}
},

预处理: $js.toString(() => {
    rule.class_name = ungzip('H4sIAAAAAAAAAwEpANb/5pel6Z+pQVYm5Zu95Lqn57O75YiXJuasp+e+jibmiJDkurrliqjmvKsjbGzbKQAAAA==')
}),
推荐: '*',
一级: '.stui-vodlist__box:has(.text-right);h4&&Text;a&&data-original;.text-right&&Text;a&&href',
搜索: '*',
二级: '*',

tab_rename: {'道长在线': '🐺在线播放'},
play_parse: true,
lazy: $js.toString(() => {
    var kcode = JSON.parse(fetch(input).match(/var player_.*?=(.*?)</)[1]);
    var kurl = kcode.url;
    if (/m3u8|mp4/.test(kurl)) {
        input = { jx: 0, parse: 0, url: kurl }
    } else {
        input = { jx: 0, parse: 1, url: input }
    }
}),

filter: 'H4sIAAAAAAAAA6vmUjJUsormqlbKTq1UslJKTixJ9UxR0lHKS8xNBfKfb9z9dF43kF+WmFMKFIiuVsoDCj9tXfGyeQVIGMgxVKrVgQg/m77g+YLGJzvWPpvW/nTt9Kc7p0KVWCCUzOnErsQSyZSlz+asgZgFs8IAXRZsDFTWXKk2tpYrVodLyYhSvxjB7Xk6e++TXctfLG97uWgizBWmcIuMKbXIGOGhNcuf7+t7uXrGsx2tMFcYwi0yodQiE4SPulY827P6aefyZ81wi4wgFnHVAgB5XHbmCQIAAA=='
}