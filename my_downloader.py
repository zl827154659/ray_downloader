import os
import sys
import warnings
import re
import requests

url = "http://www.8080s.net/movie/32088"

warnings.filterwarnings("ignore")


def down(url, dst):
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

    # "ab"表示追加形式写入文件
    with open(dst, "ab") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()

                ###这是下载实现进度显示####
                done = int(50 * temp_size / total_size)
                sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                sys.stdout.flush()
    print()  # 避免上面\r 回车符


if __name__ == '__main__':
    res = requests.get(url)
    content = res.text
    a = re.findall(r"<a[^>]*\s+href=[\'\"]?([^\'\"]*)[\'\"]?[^>]*\s+>.*<\/", content)
    down(a[0], './%s' % os.path.basename(a[0]))
