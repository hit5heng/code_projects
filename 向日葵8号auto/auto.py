import sys
import json
import requests
from PIL import Image
from io import BytesIO
import datetime
from dateutil import tz
import os
# 转换gif使用包
import imageio
import glob

class Auto:
    def __init__(self, filename=None, scale=1):
        self.conf = {
            'last_refresh_url': 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json',  # latest photo
            'img_url_pattern': 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/%id/550/%s_%i_%i.png',    # scale, time, row, col
            'scale': 1,
        }
        self.path = "./images/"
        self.filename = filename
        self.scale = scale

        # datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        self.deltatime = datetime.timedelta(minutes=10)

    def get_last_time(self):
        """
        从网站获取到的最新图像的时间数据r,
            r: <class 'requests.models.Response'>
            r.text: {"date":"2019-06-22 15:30:00","file":"PI_H08_20190622_1530_TRC_FLDK_R10_PGPFD.png"} <class 'str'>
        转换为字典resp,
            resp: <class 'dict'>
        将字典resp中的date数据转换为时间格式,
            形如2019-06-23 13:20:00, (格林威治时间), 便于转换格式和加减时间
        :return:  just like: datetime.datetime(2019, 6, 23, 13, 50)
        """
        r = requests.get(self.conf['last_refresh_url'])
        resp = json.loads(r.text)
        last_refresh_time = datetime.datetime.strptime(resp['date'], '%Y-%m-%d %H:%M:%S')
        return last_refresh_time

    def utf2local(self, utc):
        """
        获取的时间为格林威治时间utc,转换为当地时间(北京时间),用于命名等
        :param utc:  just like: datetime.datetime(2019, 6, 23, 22, 30, 28, 822914)
        :return:  just like: datetime.datetime(2019, 6, 24, 6, 30, 28, 822914, tzinfo=tzlocal())
        """
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = utc.replace(tzinfo=from_zone)
        return utc.astimezone(to_zone)

    def download(self, time):
        """
        下载到./images/目录下, 默认文件名为图像时间
        :param time:
        :param fpath:
        :param scale:
        :return:
        """
        if not os.path.exists("images"):
            os.makedirs("images") 
        png = Image.new('RGB', (550 * self.scale, 550 * self.scale))
        for row in range(self.scale):
            for col in range(self.scale):
                print('Downloading %i of %i ...' % (row * self.scale + col + 1, self.scale * self.scale))
                strtime = time.strftime("%Y/%m/%d/%H%M%S")
                url = self.conf['img_url_pattern'] % (self.scale, strtime, row, col)

                r = requests.get(url)
                # 增加超时重试功能
                # i = 0
                # while i < 3:
                #     try:
                #         r = requests.get(url, timeout=5).text
                #     except requests.exceptions.RequestException:
                #         i += 1
                # 还是没有很好的效果...还得改

                tile = Image.open(BytesIO(r.content))
                png.paste(tile, (550 * row, 550 * col, 550 * (row + 1), 550 * (col + 1)))
        if self.filename is not None:
            fpath = self.path + self.filename
        else:
            fpath = self.path + "%s.png" % self.utf2local(time).strftime("%Y/%m/%d/%H%M%S").replace('/', '')
        print('Download over, save to file %s' % fpath)
        png.save(fpath, "PNG")

    def get_last_image(self):
        print('output[%s] scale[%i]' % (self.filename, self.scale))
        time = self.get_last_time()
        self.download(time)

    def get_lastday_images(self):
        """
        获取现在前12小时的图像,共72张
        """
        for i in range(72):
            print('output[%s] scale[%i]' % (self.filename, self.scale))
            time = self.get_last_time() - self.deltatime * i
            self.download(time)

    def create_gif(self):
        """
        生成gif的函数，原始图片仅支持png
        source: 为png图片列表（排好序）
        name ：生成的文件名称
        duration: 每张图片之间的时间间隔,单位s
        """
        frames = []  # 读入缓冲区
        source = glob.glob(pathname='./images/*.png')
        source.sort()
        for img in source:
            frames.append(imageio.imread(img))
        imageio.mimsave("./images/latest_earth.gif", frames, 'GIF', duration=0.1)
        print("finished")

if __name__ == '__main__':
    a = Auto()
    a.get_lastday_images()
    a.create_gif()

