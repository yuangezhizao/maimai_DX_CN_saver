#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2021/8/2 21:42
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2021 yuangezhizao <root@yuangezhizao.cn>
"""
import mitmproxy.http
import pyperclip


class GetCookies:
    def __init__(self):
        pass

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.url == 'https://maimai.wahlap.com/maimai-mobile/home/':
            cookies = flow.response.headers.get('Set-Cookie')
            userId = cookies.split('userId=')[1].split(';')[0]
            pyperclip.copy(userId)
            print(f'userId: {userId} 已复制到剪切板')


addons = [
    GetCookies()
]
