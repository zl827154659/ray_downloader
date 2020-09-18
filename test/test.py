from concurrent.futures import ThreadPoolExecutor, as_completed
import time

task_num = 10


def download(url, dst):
    """消费者"""
    print("%s start downloading to %s " % (url, dst))
    time.sleep(2)
    return "%s has downloaded to %s " % (url, dst)


if __name__ == "__main__":
    url_list = range(1, 100)
    thread_list = []
    with ThreadPoolExecutor(max_workers=task_num) as t:
        for url in url_list:
            dst = url
            thread = t.submit(download, url, dst)
            thread_list.append(thread)

        for future in as_completed(thread_list):
            result = future.result()
