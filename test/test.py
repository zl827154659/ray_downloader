import time
import requests
import os
import sys

WET_URL_ROOT = "https://commoncrawl.s3.amazonaws.com"


def path_url(dump_id: str) -> str:
    return "/".join([WET_URL_ROOT, "crawl-data", "CC-MAIN-" + dump_id, "wet.paths.gz"])


def formatFloat(num):
    return '{:.2f}'.format(num)


def download(url, dst):
    # 第一次请求是为了得到文件总大小
    r1 = requests.get(url, stream=True, verify=False)
    total_size = int(r1.headers['Content-Length'])

    # 这重要了，先看看本地文件下载了多少
    if os.path.exists(dst):
        temp_size = os.path.getsize(dst)  # 本地已经下载的文件大小
    else:
        dst_dir = "\\".join(dst.split("\\")[:-1])
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        temp_size = 0
    if total_size <= temp_size:
        return
    # 显示一下下载了多少
    print("当前文件:%s, 已下载大小:%s" % (os.path.basename(dst), temp_size))
    print("文件总大小:%s" % total_size)
    # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
    headers = {'Range': 'bytes=%d-' % temp_size}
    # 重新请求网址，加入新的请求头的
    r = requests.get(url, stream=True, verify=False, headers=headers)

    # 设置计时器监控下载速度
    time1 = time.time()
    pre_size = 0

    # "ab"表示追加形式写入文件
    with open(dst, "ab") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()

                piece_time = time.time() - time1
                # 下载速度计算
                speed = (temp_size - pre_size) / piece_time / 1024

                # 这是下载实现进度显示
                done = int(50 * temp_size / total_size)
                sys.stdout.write("\r[%s%s] %d%%, 下载速度：%s kb/s" % (
                    '█' * done, ' ' * (50 - done), 100 * temp_size / total_size, formatFloat(speed)))
                sys.stdout.flush()
    print()  # 避免上面\r 回车符


if __name__ == "__main__":
    download_dir = os.path.abspath(os.path.join(os.getcwd(), "..", "download", "wet.path.gz"))
    download(path_url('2020-29'), download_dir)
