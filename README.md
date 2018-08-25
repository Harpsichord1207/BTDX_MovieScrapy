### 一个爬取比特大雄网电影信息的多线程爬虫

---

- 比特大雄URL： [https://www.btdx8.com/](https://www.btdx8.com/)
- 从主页出发，爬取电影页面的`url`，并简单解析电影信息，保存为`csv`
- 通过钉钉机器人发送爬取的进度
- 在`config.py`中可设置钉钉机器人`token`, `URL`的重试次数以及爬取的深度