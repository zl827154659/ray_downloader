import queue
import threading
import time

task_num = 10
queueLock = threading.Lock()
work_queue = queue.Queue(task_num)
exitFlag = 0


class DownloadThread(threading.Thread):
    def __init__(self, thread_id, q):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = q

    def run(self):
        print("开启线程： " + self.thread_id)
        print("退出线程： " + self.thread_id)


def download(thread_id, q):
    """消费者"""
    while not exitFlag:
        queueLock.acquire()
        if not work_queue.empty():
            data = q.get()
            print("线程编号 " + thread_id + "正在下载 " + data)
            time.sleep(1)
        else:
            queueLock.release()

if __name__ == "__main__":
    t = range[10]
    r = range[100]
    for i in r:
        while not work_queue.full():
            work_queue.put(i)
