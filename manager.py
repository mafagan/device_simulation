#!/usr/bin/python
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
import json

# Module to interact with mqtt broker and add task into tasklist


# Hook to transfer unicode string into normal string
def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


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
        try:
            self.load_cfg()
        except:
            print 'Load cfg failed'

    def load_cfg(self):
        opt, arg = getopt.getopt(sys.argv[1:], "c:")
        cfgfile = None

        if len(opt) != 0:
            cfgfile = opt[0][1]

        if cfgfile is not None:
            f = file(cfgfile, 'r')
            filedata = f.read()
            f.close()

            cfg_dict = json.loads(filedata, object_hook=_decode_dict)
            for projID in cfg_dict.keys():
                self.addProj(projID)
                for devName in cfg_dict[projID].keys():
                    self.addDevice(projID, devName)
                    if 'apiver' in cfg_dict[projID][devName].keys():
                        self.projSet[projID].devSet[devName] \
                            .set_ver(cfg_dict[projID][devName]['apiver'])
                    if 'cfg' in cfg_dict[projID][devName].keys():
                        self.projSet[projID].devSet[devName] \
                            .set_cfg(cfg_dict[projID][devName]['cfg'])

                    if 'app' in cfg_dict[projID][devName].keys():
                        for app in cfg_dict[projID][devName]['app'].keys():
                            self.projSet[projID].devSet[devName] \
                                .add_app(app, cfg_dict[projID][devName]['app'][app])

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
        topic = projID + '/' + devName + '/' + 'mgt'
        self.mqttc.subscribe(topic)

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

        if cmd != 'filec2d' and int(argc) != (len(lines) - 1):
            tempTask.setValidFlag(False)

        if cmd == 'filec2d' and len(lines) != 4:
            tempTask.setValidFlag(False)

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
    manager = Manager()
    try:
        manager.run()
    except KeyboardInterrupt:
        print ''
        manager.stop()
        manager.mqttc.disconnect()
        print 'Manager loop exit.'
        manager.taskThread.stop()
        manager.taskThread.join()
