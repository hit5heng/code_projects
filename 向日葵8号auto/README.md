
# 向日葵8号
- 向日葵8号,每10分钟更新一次图像,最新的图像为10分钟之前的，格林威治时间
- 具体可以查看http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json
    - 格式如`{"date":"2019-06-22 15:20:00","file":"PI_H08_20190622_1520_TRC_FLDK_R10_PGPFD.png"}`

## 参考
- 下载最新图像 >>> [GITHUB](https://github.com/liuwons/himawari8downloader)
- Python 定时获取卫星图像做为桌面背景(爬虫获取) >>> [GITHUB](https://github.com/StuPeter/Auto_Wallpaper_spider)
    
- 实时壁纸(windows?)  >>> [GITHUB](https://github.com/Cheain/wallpaper)
- Ubuntu桌面自动生成新的壁纸列表的Python脚本 >>> [GITHUB](https://blog.csdn.net/moqsien/article/details/80260046)
- 下载png，转换为gif >>> [GITHUB](https://www.cnblogs.com/dcb3688/p/4608048.html)

### [链接解析]((https://github.com/StuPeter/Auto_Wallpaper_spider))
原始图片链接(通过chrome浏览器查看元素) http://himawari8-dl.nict.go.jp/himawari8/img/D531106/thumbnail/550/2018/09/26/063000_0_0.png

链接段|意思（猜的）
--|--
http://himawari8-dl.nict.go.jp/|网站域名
himawari8/|卫星名字：向日葵8号
img/|图片
D531106/	|布吉岛
thumbnail/	|布吉岛
550/	|卫星图像像素
2018/09/26/	|卫星图像日期
063000_0_0	|卫星图像时间（GMT：格林威治标准时间)
.png	|图像格式（GMT：格林威治标准时间)

## 通过放大,看到图片链接
- 2倍图片(第一行第一张): http://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/2019/06/21/010000_0_0.png ...
- 4倍图片(第二行第一张): http://himawari8-dl.nict.go.jp/himawari8/img/D531106/4d/550/2019/06/21/010000_1_0.png ...
- ...

根据https://github.com/liuwons/himawari8downloader 中的The result image's width and height are both scale×550. scale can be 1, 2, 4, 8, 16, 20.
推测:
- 链接中段新增的 /xd/ 可以通过更改x的值[1, 2, 4, 8, 16, 20]改变图像大小,
- 缩略图片（1倍），中间可以是1d，也可以是thumbnail

- 放大图像是由550x550的图像拼接而成, 每张图片后段为 010000_x_y.png, x为第几行,y为第几列
  - 例: 2倍图像为2x2x(550x550), 后段分别为
    ```
    010000_0_0.png, 010000_0_1.png
    010000_1_0.png, 010000_1_1.png
    ```
  - 4倍,8倍等同理


链接段|意思（我猜的）
--|--
http://himawari8-dl.nict.go.jp/|网站域名
himawari8/|卫星名字：向日葵8号
img/|图片
D531106/	|布吉岛
xd/或者为thumbnail(缩略图)	|放大倍数,x=1，2,4,8,16,20
550/	|卫星图像像素
2018/09/26/	|卫星图像日期
063000_0_0	|卫星图像时间（格林威治标准时间)
.png	|图像格式

![gif](./images/latest_earth.gif)
