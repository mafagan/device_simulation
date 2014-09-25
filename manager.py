import threading
import checkThread
import mosquitto
import macro
import proj
import random
import task
import sys
import getopt
import os


class Manager:
    def __init__(self):
        self.tasklist = []
        self.tlLock = threading.Lock()
        self.devSet = {}
        self.projSet = {}
        self.mqttc = mosquitto.Mosquitto()
        self.taskThread = checkThread.ckThread(self.tlLock, self.tasklist,
                                               self.mqttc, self.projSet)
        self.flag = False

        self.taskThread.start()
        self.mqttc.connect(macro.MQTT_BROKER_IP, macro.MQTT_BROKER_PORT,
                           60, True)
        self.mqttc.on_message = self.on_message
        self.checkFSDir()

    def checkFSDir(self):
        path = sys.path[0] + '/filesystem'

        if not (os.path.exists(path)):
            os.makedirs(path)

    def addProj(self, projID):
        if projID in self.projSet:
            pass
        else:
            self.projSet[projID] = proj.proj(projID)

    def addDevice(self, projID, devName):
        if not (projID in self.projSet):
            self.addProj(projID)

        self.projSet[projID].addDevice(devName)
        self.mqttc.subscribe(projID+'/'+devName+'/'+'mgt')

    def on_message(self, mosq, obj, msg):
        topic = msg.topic
        payload = msg.payload

        print topic + ': ' + payload
        topic_list = topic.split('/')
        projID = topic_list[0]
        dev = topic_list[1]

        lines = payload.split('\r\n')

        while '' in lines:
            lines.remove('')

        orderList = lines[0].split(' ')
        serNumber = orderList[1]
        cmd = orderList[2]
        argc = orderList[3]
        delay = None
        tempTask = task.task()

        tempTask.setProjID(projID)
        tempTask.setSerNumber(serNumber)
        tempTask.setDevice(dev)
        tempTask.setOperation(cmd)

        if int(argc) != (len(lines) - 1):
            return

        lines[0] = int(argc)
        tempTask.setArgs(lines)

        if not (cmd in macro.cmd_list.keys()):
            print 'cmd "' + cmd + '" not exist'
            return

        delay = random.randint(macro.cmd_delay[macro.cmd_list[cmd]][0],
                               macro.cmd_delay[macro.cmd_list[cmd]][1])
        tempTask.setDelay(delay)

        self.tlLock.acquire()
        self.tasklist.append(tempTask)
        self.tlLock.release()

    def run(self):
        self.flag = True
        while self.flag:
            self.mqttc.loop()

    def stop(self):
        self.flag = False

if __name__ == '__main__':
    opt, arg = getopt.getopt(sys.argv[1:], "c:")
    cfgfile = None

    if len(opt) != 0:
        cfgfile = opt[0][1]

    manager = Manager()
    manager.addDevice('demo', 'dev')
    try:
        manager.run()
    except KeyboardInterrupt:
        print ''
        manager.stop()
        manager.mqttc.disconnect()
        print 'Manager loop exit.'
        manager.taskThread.stop()
        manager.taskThread.join()
