import threading
import checkThread
import mosquitto
import macro
import proj
import random
import task


class Manager:
    def __init__(self):
        self.tasklist = []
        self.tlLock = threading.Lock()
        self.devSet = {}
        self.projSet = {}
        self.mqttc = mosquitto.Mosquitto()
        self.taskThread = checkThread.ckThread(self.tlLock, self.tasklist,
                                               self.mqttc)
        self.flag = False

        self.taskThread.start()
        self.mqttc.connect(macro.MQTT_BROKER_IP, macro.MQTT_BROKER_PORT,
                           60, True)
        self.mqttc.on_message = self.on_message

    def addProj(self, projID):
        if projID in self.projSet:
            pass
        else:
            self.projSet[projID] = proj.proj(projID)

    def addDevice(self, projID, devName):
        if not (projID in self.projSet):
            self.addProj(projID)

        self.projSet[projID].addDevice(devName)
        self.mqttc.subscribe(self.projID+'/'+devName+'/'+'mgt')

    def on_message(self, msg):
        topic = msg.topic
        payload = msg.payload

        print topic + ': ' + payload
        topic_list = topic.split('/')
        projID = topic_list[0]
        dev = topic_list[1]

        lines = payload.split('\r\n')
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

        if cmd == macro.cmd[macro.GETVER]:
            delay = random.randint(macro.cmd_delay[macro.GETVER][0],
                                   macro.cmd_delay[macro.GETVER][1])

        elif cmd == macro.cmd[macro.GETCFG]:
            delay = random.randint(macro.cmd_delay[macro.GETCFG][0],
                                   macro.cmd_delay[macro.GETCFG][1])

        elif cmd == macro.cmd[macro.GETAPPLIST]:
            delay = random.randint(macro.cmd_delay[macro.GETAPPLIST][0],
                                   macro.cmd_delay[macro.GETAPPLIST][1])

        elif cmd == macro.cmd[macro.GETAPILIST]:
            delay = random.randint(macro.cmd_delay[macro.GETAPILIST][0],
                                   macro.cmd_delay[macro.GETAPILIST][1])

        elif cmd == macro.cmd[macro.GETAPPLIST]:
            delay = random.randint(macro.cmd_delay[macro.GETAPPLIST][0],
                                   macro.cmd_delay[macro.GETAPPLIST][1])

        elif cmd == macro.cmd[macro.SETCFG]:
            delay = random.randint(macro.cmd_delay[macro.SETCFG][0],
                                   macro.cmd_delay[macro.SETCFG][1])

        elif cmd == macro.cmd[macro.PING]:
            delay = random.randint(macro.cmd_delay[macro.PING][0],
                                   macro.cmd_delay[macro.PING][1])

        elif cmd == macro.cmd[macro.STARTAPP]:
            delay = random.randint(macro.cmd_delay[macro.STARTAPP][0],
                                   macro.cmd_delay[macro.STARTAPP][1])

        elif cmd == macro.cmd[macro.STOPAPP]:
            delay = random.randint(macro.cmd_delay[macro.STOPAPP][0],
                                   macro.cmd_delay[macro.STOPAPP][1])

        elif cmd == macro.cmd[macro.SYSTEM]:
            delay = random.randint(macro.cmd_delay[macro.SYSTEM][0],
                                   macro.cmd_delay[macro.SYSTEM][1])

        elif cmd == macro.cmd[macro.REBOOT]:
            delay = random.randint(macro.cmd_delay[macro.REBOOT][0],
                                   macro.cmd_delay[macro.REBOOT][1])

        elif cmd == macro.cmd[macro.UPDATEFM]:
            delay = random.randint(macro.cmd_delay[macro.UPDATEFM][0],
                                   macro.cmd_delay[macro.UPDATEFM][1])

        elif cmd == macro.cmd[macro.INSTALLAPP]:
            delay = random.randint(macro.cmd_delay[macro.INSTALLAPP][0],
                                   macro.cmd_delay[macro.INSTALLAPP][1])

        elif cmd == macro.cmd[macro.FILEC2D]:
            delay = random.randint(macro.cmd_delay[macro.FILEC2D][0],
                                   macro.cmd_delay[macro.FILEC2D][1])

        elif cmd == macro.cmd[macro.FILED2C]:
            delay = random.randint(macro.cmd_delay[macro.FILED2C][0],
                                   macro.cmd_delay[macro.FILED2C][1])

        elif cmd == macro.cmd[macro.RPCCALL]:
            delay = random.randint(macro.cmd_delay[macro.RPCCALL][0],
                                   macro.cmd_delay[macro.RPCCALL][1])
        else:
            return

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
