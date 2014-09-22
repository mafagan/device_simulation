import threading
import time


class ckThread(threading.Thread):
    def __init__(self, lock, tasklist):
        super(ckThread, self).__init__(name='ckThread')
        self.lock = lock
        self.flag = False
        self.tasklist = tasklist

    def run(self):
        self.flag = True

        while self.flag:
            time.sleep(1/1000.0)
            curtime = (int)(time.time())
            for i in self.tasklist:
                if(curtime > i.endtime):
                    pass

    def stop(self):
        self.flag = False
