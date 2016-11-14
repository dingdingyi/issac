# coding=utf8
# author=PlatinumGod
# created on 2016/11/12

import requests
import logging
import re
import config
import threading
import Queue

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


class Fetcher(threading.Thread):

    def __init__(self, taskqueue, resultqueue, timeout=None, retry=None):
        """
        :param taskqueue: 任务队列
        :param resultqueue: 结果队列
        :param timeout: 超时
        :param retry: 重试次数
        """
        super(Fetcher, self).__init__()
        self.taskqueue = taskqueue
        self.resultqueue = resultqueue
        if timeout is None:
            self.timeout = 10
        else:
            self.timeout = timeout
        if retry is None:
            self.retry = 3
        else:
            self.retry = retry
        self.url = ''
        self.compilers = []
        self.setDaemon(True)
        self.start()

    def run(self):
        while not self.taskqueue.empty():
            url, patterns = self.taskqueue.get()
            print url, patterns
            self._initfetcher(url, patterns)
            self.gethtml()
            self.parse()

    def _initfetcher(self, url, patterns):
        # 一个正则表达式列表(patterns)包含三个元素：
        # 1-一个正则匹配的表达式，
        # 2-一个用来指示是否为严格模式匹配的bool值
        # 3-一个目标信息的描述，如果描述是以TASK开头，将匹配结果加入任务队列，如果以RESULT开头，将其放入结果队列
        self.url = url
        for pattern, strict, descrption in patterns:
            if strict:
                compiler = re.compile(pattern=pattern)
            else:
                compiler = re.compile(pattern=pattern, flags=re.S)
            self.compilers.append([compiler, descrption])
        logging.info("__initialize Fetcher for url ---", url)

    def gethtml(self):
        """
        :return: self.url的网页源码
        """
        while self.retry > 0:
            self.retry -= 1
            req = requests.get(
                url=self.url,
                timeout=self.timeout,
                headers=headers)
            try:
                self.sourcecode = req.content
                if req.status_code == 200:
                    logging.debug("Success to fetch %s", self.url)
                else:
                    logging.error(
                        "Unable to fetch %s, httpcode: %d, retry time: %d",
                        self.url,
                        req.status_code,
                        self.retry)
            except:
                logging.error(
                    "Unhandled exception happend while fetching %s, retry time: %d",
                    self.url,
                    self.retry)

    def parse(self):
        if not self.compilers:
            raise RuntimeError("Uninit Fecther...")
        result = task = {}
        for compiler, descrption in self.compilers:
            try:
                res = compiler.findall(self.sourcecode)
                if res is not None:
                    if descrption[:4] == 'TASK':
                        task[descrption[4:]] = res
                    elif descrption[:6] == 'RESULT':
                        result[descrption[6:]] = res
            except:
                continue
        for key, value in result.items():
            print key
            for v in value:
                print v


if __name__ == '__main__':
    task = Queue.Queue()
    result = Queue.Queue
    x = ('https://www.zhihu.com/people/TuringDon/', config.patterns)
    task.put(x)
    test = Fetcher(task, result)
    a = raw_input("wait...")
