#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2021/8/2 21:42
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2021 yuangezhizao <root@yuangezhizao.cn>
"""
import mitmproxy.http


class GetCookies:
    def __init__(self):
        pass

    def request(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.url == 'https://maimai.wahlap.com/maimai-mobile/home/':
            print(flow.request.cookies)


addons = [
    GetCookies()
]
