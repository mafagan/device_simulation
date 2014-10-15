#!/usr/bin/python
import threading
import time

# Thread to check tasklist and excute task in it


class ckThread(threading.Thread):
    def __init__(self, lock, tasklist, mqttc, projSet):
        super(ckThread, self).__init__(name='ckThread')
        self.lock = lock
        self.flag = False
        self.tasklist = tasklist
        self.mqttc = mqttc
        self.projSet = projSet

    def run(self):
        self.flag = True

        while self.flag:
            time.sleep(1/1000.0)
            self.lock.acquire()

            curtime = time.time()
            for i in self.tasklist:
                if not i.flag:
                    self.send_res_bc(i, None)
                    continue
                if(curtime > i.endtime):
                    try:
                        res = (self.projSet[i.projID].devSet[i.device]) \
                            .cmd_exec(i.operation, i.args)
                    except:
                        pass
                    self.send_res_bc(i, res)
                    self.tasklist.remove(i)

            self.lock.release()
        print 'Check thread exit.'

# Send information back to Cloud

    def send_res_bc(self, task, res):
        ret_path = task.projID + '/' + task.device + '/dp_1/dat'

        if res is None:
            self.mqttc.publish(ret_path, 'EC1 ' + task.serNumber + ' '
                               + str(-10005) + ' ' + str(0) + '\r\n')
            return

        ret_str = 'EC1 ' + task.serNumber + ' ' + str(res[0]) + ' ' \
            + str(res[1]) + '\r\n'

        for i in range(2, len(res)):
            ret_str = ret_str + res[i]

        print 'pub:\n' + ret_path + '\n' + ret_str
        self.mqttc.publish(ret_path, ret_str)

    def stop(self):
        self.flag = False
