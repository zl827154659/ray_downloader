import requests, re
from progress import *


host = "http://www.8080s.net"
url = "http://www.8080s.net/movie/32088"
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}

''' 断点下载'''


def down(url, dst):
    try:
        # 第一次请求为了获取文件大小
        response = requests.get(url, stream=True, verify=False)
        file_size = int(response.headers['content-length'])
        if os.path.exists(dst):
            first_size = os.path.getsize(dst)
        else:
            dst_dir = "\\".join(dst.split("\\")[:-1])
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            first_size = 0
        if file_size <= first_size:
            return
        headers['Range'] = "bytes=%d-" % (first_size,)
        print("开始下载：" + url)
        res = requests.get(url, stream=True, headers=headers, verify=False)
        # 以ab模式打开则为追加写入
        with open(dst, "ab") as f:
            dp = DownProgress(file_size, first_size, dst)
            dp.start()
            chunk_size = 1024
            for chunk in res.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    dp.update(chunk_size)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    res = requests.get(url)
    content = res.text
    a = re.findall(r"<a[^>]*\s+href=[\'\"]?([^\'\"]*)[\'\"]?[^>]*\s+>.*<\/", content)
    down(a[0], './%s' % os.path.basename(a[0]))