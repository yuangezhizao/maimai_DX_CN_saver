# maimai_DX_CN_saver
舞萌数据存储

### 简介
数据提取使用 lxml 配合 xpath，脚本不能裸跑需 Flask 环境

代码写的很屎，凑合看吧。。。

### 页面适配
- [x] 主页（home）
- [x] 游戏数据（playerData）
  - [x] 游戏数据（playerData）
  - [x] 相册（album）
- [x] 记录（record）
  - [x] 游戏记录（record）
    - [x] 详细（playlogDetail）
  - [ ] 乐曲成绩（musicGenre）
- [ ] 排行榜（ranking）

### 相关项目
[mainetcn](https://github.com/Astrian/mainetcn)：`Cookie`中`userId`的解释非常详细，以至于自己的项目都懒得再写了

[maimaidx-prober](https://github.com/Diving-Fish/maimaidx-prober)：都拿`Go`写了个抓包工具，实在是太硬核了
