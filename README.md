# maimai_DX_CN_saver

舞萌数据存储

### 简介

懒得每次开`Charles`抓包复制`userId`，用`mitmproxy`复制到剪切板他不香嘛？

### 安装[mitmproxy](https://github.com/mitmproxy/mitmproxy)

参照：https://docs.mitmproxy.org/stable/overview-installation

### 配置证书

参照：https://docs.mitmproxy.org/stable/overview-getting-started/#configure-your-browser-or-device

### 使用

``` bash
mitmdump -s addons.py
```

### 页面适配（Ver.CH1.11-F）

- [x] 主页（home）
- [x] 游戏数据
    - [x] 游戏数据（playerData）
    - [x] 相册（playerData_album）
- [x] 记录
    - [x] 游戏记录（record）
        - [x] 详细（record_playlogDetail）
    - [ ] 乐曲成绩（musicGenre）
- [ ] 排行榜（ranking）

### 原始代码

1. https://github.com/yuangezhizao/maimai_DX_CN_probe/blob/main/src/maimai_DX_CN_probe/models/maimai.py
2. https://github.com/yuangezhizao/maimai_DX_CN_probe/blob/main/src/maimai_DX_CN_probe/plugins/wechat_saver.py

### 相关项目

- [mainetcn](https://github.com/Astrian/mainetcn)：`Cookie`中`userId`的解释非常详细，以至于自己的项目都懒得再写了
- [maimaidx-prober](https://github.com/Diving-Fish/maimaidx-prober)：都拿`Go`写了个抓包工具，实在是太硬核了
