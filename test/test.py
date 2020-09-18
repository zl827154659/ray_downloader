from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse


def download(url, dst):
    """消费者"""
    print("%s start downloading to %s " % (url, dst))
    time.sleep(2)
    return "%s has downloaded to %s " % (url, dst)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump", help="the dump_id of common crawl wet file", default="2017-51")
    parser.add_argument("--task_num", help="the number of multiprocessing downloading threads", default=10)
    args = parser.parse_args()
    url_list = range(1, 100)
    thread_list = []
    with ThreadPoolExecutor(max_workers=int(args.task_num)) as t:
        for url in url_list:
            dst = url
            thread = t.submit(download, "dump_id : " + args.dump + "  url : " + str(url), dst)
            thread_list.append(thread)

        for future in as_completed(thread_list):
            result = future.result()
