import mosquitto
import macro
import threading
import os


topic = 'demo/dev01/mgt'


class input_thread(threading.Thread):
    def __init__(self, mqttc, topic):
        super(input_thread, self).__init__(name='input_thread')
        self.topic = topic
        self.mqttc = mqttc
        self.flag = False

    def run(self):
        self.flag = True
        while self.flag:
            order = raw_input('type command:\n')
            if order == 'q':
                break
            orderList = order.split(' ')
            if len(orderList) == 0:
                continue
            msg = 'EC1 123456789 ' + orderList[0] + \
                ' ' + str(len(orderList)-1) + '\r\n'

            for i in range(1, len(orderList)):
                msg = msg + orderList[i] + '\r\n'

            self.send_msg(msg)

    def send_msg(self, msg):
        self.mqttc.publish(self.topic, msg)

    def stop(self):
        self.flag = False


def on_message(mosq, obj, msg):
    payload = msg.payload
    lines = payload.split('\r\n')
    while '' in lines:
        lines.remove('')
    print lines
    if len(lines) != 3:
        print 'Failed'
        return
    filedata = lines[2][:-1]
    f = file('./file_recv', 'wb')
    filedata = f.write(filedata)
    f.close()

if __name__ == '__main__':
    mqttc = mosquitto.Mosquitto()
    mqttc.connect(macro.MQTT_BROKER_IP, macro.MQTT_BROKER_PORT, 60, True)
    mqttc.subscribe('demo/dev01/mgtr')
    mqttc.on_message = on_message

    f = file('main', 'rb')
    filedata = f.read()
    f.close()
    size = os.path.getsize('main')

    pubstr = 'EC1 123456789 filed2c 1\r\n/tmp/sth.bin\r\n'
    mqttc.publish(topic, pubstr)
    try:
        mqttc.loop_forever()
    except KeyboardInterrupt:
        mqttc.disconnect()
        print 'test exit'
