#!/usr/bin/python
import threading
import checkThread
import mosquitto
import macro
import proj
import random
import task
import sys
import os
import json
import ConfigParser

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
        bingo_flag = True
        self.tasklist = []
        self.tlLock = threading.Lock()
        self.projSet = {}
        self.mqtt_broker_host = macro.MQTT_BROKER_HOST
        self.mqtt_broker_port = macro.MQTT_BROKER_PORT
        self.simfile = None
        self.flag = False
        self.latency = {}
        self.failure = {}

        self.checkFSDir()
        try:
            self.load_conf()
            self.load_simfile()
        except:
            print 'Load cfg failed'
            bingo_flag = False

        self.mqttc = mosquitto.Mosquitto()
        self.mqttc.connect(self.mqtt_broker_host, self.mqtt_broker_port,
                           60, True)
        self.mqttc.on_message = self.on_message
        self.sub_topic()
        self.taskThread = checkThread.ckThread(self.tlLock, self.tasklist,
                                               self.mqttc, self.projSet)
        self.taskThread.start()

        if bingo_flag:
            print 'Init success!'

    def load_conf(self):
        conf_file = macro.conf_file
        cf = ConfigParser.ConfigParser()
        latency_flag = 0
        failure_flag = 2

        cf.read(conf_file)

        host = cf.get('conf', 'mqtt_host')
        port = cf.get('conf', 'mqtt_port')
        latency = cf.get('conf', 'latency')
        failure = cf.get('conf', 'failure')
        simfile = cf.get('conf', 'simfile')

        if host is not None:
            self.mqtt_broker_host = host

        if port is not None:
            self.mqtt_broker_port = port

        if latency == 'low':
            latency_flag = 1

        if failure == 'low':
            failure_flag = 3

        self.simfile = simfile

        data_dict = {}
        data_dict['getver'] = cf.get('latency_and_failure', 'getver').split(' ')
        data_dict['getapplist'] = cf.get('latency_and_failure', 'getapplist').split(' ')
        data_dict['getcfg'] = cf.get('latency_and_failure', 'getcfg').split(' ')
        data_dict['setcfg'] = cf.get('latency_and_failure', 'setcfg').split(' ')
        data_dict['ping'] = cf.get('latency_and_failure', 'ping').split(' ')
        data_dict['startapp'] = cf.get('latency_and_failure', 'startapp').split(' ')
        data_dict['stopapp'] = cf.get('latency_and_failure', 'stopapp').split(' ')
        data_dict['system'] = cf.get('latency_and_failure', 'system').split(' ')
        data_dict['reboot'] = cf.get('latency_and_failure', 'reboot').split(' ')
        data_dict['updatefirmware'] = cf.get('latency_and_failure', 'updatefirmware').split(' ')
        data_dict['installapp'] = cf.get('latency_and_failure', 'installapp').split(' ')
        data_dict['filec2d'] = cf.get('latency_and_failure', 'filec2d').split(' ')
        data_dict['filed2c'] = cf.get('latency_and_failure', 'filed2c').split(' ')
        data_dict['rpccall'] = cf.get('latency_and_failure', 'rpccall').split(' ')

        for key in data_dict.keys():
            while '' in data_dict[key]:
                data_dict[key].remove('')

            macro.cmd_delay[macro.cmd_list[key]] = int(data_dict[key][latency_flag])
            macro.cmd_fail_percent[macro.cmd_list[key]] = int(data_dict[key][failure_flag])

    def load_simfile(self):
        if self.simfile is not None:
            f = file(self.simfile, 'r')

            if f is None:
                print 'Sim file not exist'
                return

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

    def sub_topic(self):
        for projID in self.projSet:
            for dev in self.projSet[projID].devSet:
                topic = projID + '/' + dev + '/' + 'mgt'
                self.mqttc.subscribe(topic)

    def addProj(self, projID):
        if projID in self.projSet:
            pass
        else:
            self.projSet[projID] = proj.proj(projID)

    def addDevice(self, projID, devName):
        if not (projID in self.projSet):
            self.addProj(projID)
        self.projSet[projID].addDevice(devName)

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
        if len(orderList) < 4:
            print 'Invalid command: ' + orderList
            return

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
        delay = random.randint(macro.cmd_delay[macro.cmd_list[cmd]]-macro.deviation,
                               macro.cmd_delay[macro.cmd_list[cmd]]+macro.deviation)
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
    except BaseException, e:
        print e.args
    finally:
        manager.stop()
        manager.mqttc.disconnect()
        print 'Manager loop exit.'
        manager.taskThread.stop()
        manager.taskThread.join()
