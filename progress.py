import os
import time
from threading import Thread

'''下载进度条'''


class DownProgress(object):

    def __init__(self, total, init_size, dst):
        # 文件总大小
        self.total = total
        # 下载大小
        self.init_size = init_size
        # 文件保存路径
        self.dst = dst

    def start(self):
        def start():
            start_time = time.time()
            print('[文件大小]：%.2f MB' % ((self.total - self.init_size) / 1024 / 1024))

            while self.init_size < self.total:
                speed_str = ''
                if os.path.exists(self.dst):
                    # 计算下载率
                    start = self.init_size
                    time.sleep(1)
                    down_speed = (self.init_size - start) / 1024
                    if down_speed > 1024:
                        speed_str = '%.2f MB/s' % (down_speed / 1024)
                    else:
                        speed_str = '%.2f kb/s' % down_speed
                    filename = os.path.basename(self.dst)
                    print('\r' + '[%s  下载进度]：[%s]%.2f%%，下载速度：%s' % (filename,
                    '#' * int(self.init_size * 50 / self.total), float(self.init_size / self.total * 100), speed_str),
                          end='')

            # 计算下载时间
            offset_time = time.time() - start_time
            if offset_time > 60:
                offset_time = '%.2f 分钟' % (offset_time / 60)
            else:
                offset_time = '%.2f 秒' % offset_time
            print('\n' + '下载完成，耗时：%s' % offset_time)

        th = Thread(target=start)
        th.start()

    ''' 更新下载大小'''

    def update(self, size):
        self.init_size += size

if __name__ == "__main__":
    print(os.path.abspath(os.path.join(os.getcwd(), "..", "CommonCrawl")))
    print(os.path.join(os.getcwd(), "..", "CommonCrawl"))
