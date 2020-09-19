import gzip
import argparse
import threading
from my_downloader import *
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

WET_URL_ROOT = "https://commoncrawl.s3.amazonaws.com"
# download_dir = os.path.join(os.getcwd(), "download")
download_dir = os.path.abspath(os.path.join(os.getcwd(), "..", "CommonCrawl"))


def path_url(dump_id: str) -> str:
    return "/".join([WET_URL_ROOT, "crawl-data", "CC-MAIN-" + dump_id, "wet.paths.gz"])


def path_download(dump_id: str):
    dst = os.path.join(download_dir, dump_id, "wet.paths.gz")
    try:
        down(path_url(dump_id), dst)
    except Exception as e:
        print(e)


def path_file_reader(dump_id: str):
    """
    :param dump_id: 文件集编号
    :return: 路径文件的io

    打开路径文件，按照url索引集准备下载列表
    """
    filename = os.path.join(download_dir, dump_id, "wet.paths.gz")
    # 如果路径文件不存在，则重新下载路径文件再打开
    if not os.path.exists(filename):
        print("the 'wet.paths.gz' file is not exist, will download soon")
        path_download(dump_id)
    return gzip.open(Path(filename), "rt")


def segments_download(dump_id: str, task_num: int):
    with path_file_reader(dump_id) as f:
        segments = [segment.strip() for segment in f]
    n = len(segments)
    thread_list = []
    with ThreadPoolExecutor(max_workers=task_num) as t:
        for i, segment in enumerate(segments):
            segment_url = "/".join((WET_URL_ROOT, segment))
            dst = os.path.join(download_dir, dump_id, os.path.basename(segment_url))
            thread = t.submit(down, segment_url, dst)
            thread_list.append(thread)
        for future in as_completed(thread_list):
            result = future.result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump", help="the dump_id of common crawl wet file", default="2020-29")
    parser.add_argument("--task_num", help="the number of multiprocessing downloading threads", default=100)
    args = parser.parse_args()
    path_download(str(args.dump))
    segments_download(str(args.dump), int(args.task_num))
