import threading
import time


class ckThread(threading.Thread):
    def __init__(self, lock, tasklist, mqttc):
        super(ckThread, self).__init__(name='ckThread')
        self.lock = lock
        self.flag = False
        self.tasklist = tasklist
        self.mqttc = mqttc

    def run(self):
        self.flag = True

        while self.flag:
            time.sleep(1/1000.0)
            self.lock.acquire()

            curtime = (int)(time.time())
            for i in self.tasklist:
                if(curtime > i.endtime):
                    res = i.device.cmd_exec(i.operation, i.args)
                    self.send_res_bc(i, res)
                    self.tasklist.remove(i)

            self.lock.release()
        print 'Check thread exit.'

    def send_res_bc(self, task, res):
        ret_path = task.projID + '/' + task.device + '/mgtr'
        ret_str = 'EC1 ' + task.serNumber + ' ' + str(res[0]) + ' ' \
            + str[res[1]] + '\r\n'

        for i in range(2, 2+res[1]):
            ret_str = ret_str + res[i]

        self.mqttc.publish(ret_path, ret_str)

    def stop(self):
        self.flag = False
