import gzip
from my_downloader import *
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

WET_URL_ROOT = "https://commoncrawl.s3.amazonaws.com"
download_dir = os.getcwd() + "\\" + "download"
task_num = 10


def path_url(dump_id: str) -> str:
    return "/".join([WET_URL_ROOT, "crawl-data", "CC-MAIN-" + dump_id, "wet.paths.gz"])


def path_download(dump_id: str):
    dst = download_dir + "\\" + dump_id + "\\" + "wet.paths.gz"
    print(dst)
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
    filename = download_dir + "\\" + dump_id + "\\wet.paths.gz"
    if isinstance(filename, str):
        return gzip.open(Path(filename), "rt")
    # 如果路径文件不存在，则重新下载路径文件再打开
    print("the 'wet.paths.gz' file is not exist, will download soon")
    path_download(dump_id)
    return path_file_reader(dump_id)


def segments_download(dump_id: str):
    with path_file_reader(dump_id) as f:
        segments = [segment.strip() for segment in f]
    n = len(segments)
    thread_list = []
    with ThreadPoolExecutor(max_workers=task_num) as t:
        for i, segment in enumerate(segments):
            segment_url = "/".join((WET_URL_ROOT, segment))
            dst = download_dir + "\\" + dump_id + "\\" + os.path.basename(segment_url)
            thread = t.submit(down, segment_url, dst)
            thread_list.append(thread)
        for future in as_completed(thread_list):
            result = future.result()


if __name__ == "__main__":
    segments_download("2017-51")
