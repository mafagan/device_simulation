import mosquitto
import macro
import threading
import time
import os


topic = 'demo/dev01/mgt'
proj_base = 'demo'
dev_base = 'dev'

ece = 'EC1 '


def getver():
    res = ece + str(int(time.time())) + ' getver 0\r\n'
    return res


def getapplist():
    res = ece + str(int(time.time())) + ' getapplist 0\r\n'
    return res


def getcfg():
    res = ece + str(int(time.time())) + ' getcfg 0\r\n'
    return res


def ping():
    res = ece + str(int(time.time())) + ' ping 0\r\n'
    return res


def reboot():
    res = ece + str(int(time.time())) + ' reboot 0\r\n'
    return res


def setcfg(cfg_str):
    res = ece + str(int(time.time())) + ' setcfg 1\r\n' + cfg_str + '\r\n'
    return res


def startapp(appname):
    res = ece + str(int(time.time())) + ' startapp 1\r\n' + appname + '\r\n'
    return res


def stopapp(appname):
    res = ece + str(int(time.time())) + ' stopapp 1\r\n' + appname + '\r\n'
    return res


def updatefirmware(addr):
    res = ece + str(int(time.time())) + ' updatefirmware 1\r\n' + addr + '\r\n'
    return res


def installapp(appname):
    res = ece + str(int(time.time())) + ' installapp 1\r\n' + appname + '\r\n'
    return res


def filec2d(filepath, filesrc):
    res = ece + str(int(time.time())) + ' filec2d 2\r\n' + filepath + '\r\n'
    fp = file(filesrc, 'rb')
    filedata = fp.read()
    fp.close()
    size = os.path.getsize(filesrc)

    res = res + '\\x1B' + str(size) + '\r\n'
    res = res + filedata + '\r\n'
    return res


def filed2c(filepath):
    res = ece + str(int(time.time())) + ' filed2c 1\r\n' + filepath + '\r\n'
    return res


def system(cmd):
    return None


def systemcall():
    pass


api_itm = {
    1: getver,
    2: getcfg,
    3: getapplist,
    4: ping,
    5: reboot,
    6: setcfg,
    7: startapp,
    8: stopapp,
    9: updatefirmware,
    10: installapp,
    11: filec2d,
    12: filed2c
}


class input_thread(threading.Thread):
    def __init__(self, mqttc):
        super(input_thread, self).__init__(name='input_thread')
        self.mqttc = mqttc
        self.flag = False

    def run(self):
        self.flag = True
        while self.flag:
            in_data = raw_input()
            in_data = in_data.split(' ')
            topic = proj_base + in_data[0] + '/' + dev_base + in_data[1] \
                + '/mgt'
            msg = None
            cmd = in_data[2]
            if cmd == 'getver':
                msg = getver()
            elif cmd == 'getapplist':
                msg = getapplist()
            elif cmd == 'getcfg':
                msg = getcfg()
            elif cmd == 'ping':
                msg = ping()
            elif cmd == 'reboot':
                msg = reboot()
            elif cmd == 'setcfg':
                msg = setcfg(in_data[3])
            elif cmd == 'startapp':
                msg = startapp(in_data[3])
            elif cmd == 'stopapp':
                msg = stopapp(in_data[3])
            elif cmd == 'updatefirmware':
                msg = updatefirmware(in_data[3])
            elif cmd == 'installapp':
                msg = installapp(in_data[3])
            elif cmd == 'filec2d':
                msg = filec2d(in_data[3], in_data[4])
            elif cmd == 'filed2c':
                msg = filed2c(in_data[3])
            else:
                print 'Invalid command!'

            if msg is not None:
                self.mqttc.publish(topic, msg)

    def send_msg(self, msg):
        self.mqttc.publish(self.topic, msg)

    def stop(self):
        self.flag = False


def on_message(mosq, obj, msg):
    print msg.topic + ':\n' + msg.payload


if __name__ == '__main__':
    mqttc = mosquitto.Mosquitto()
    mqttc.connect(macro.MQTT_BROKER_IP, macro.MQTT_BROKER_PORT, 60, True)

    for pid in range(1, 50+1):
        for did in range(1, 50+1):
            mqttc.subscribe('demo'+str(pid)+'/dev'+str(did)+'/mgtr')
    mqttc.on_message = on_message

    it = input_thread(mqttc)
    try:
        it.start()
        mqttc.loop_forever()
    except KeyboardInterrupt:
        mqttc.disconnect()
        it.stop()
        it.join()
        print 'test exit'
