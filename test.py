import mosquitto
import macro
import threading

topic = 'demo/dev/mgt'


class input_thread(threading.Thread):
    def __init__(self, mqttc, topic):
        super(input_thread, self).__init__(name='input_thread')
        self.topic = topic
        self.mqttc = mqttc

    def run(self):

        while True:
            order = raw_input('type command')
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


def on_message(msg):
    print msg.topic + ': ' + msg.payload


if __name__ == '__main__':
    mqttc = mosquitto.Mosquitto()
    mqttc.connect(macro.MQTT_BROKER_IP, macro.MQTT_BROKER_PORT, 60, True)
    mqttc.subscribe('demo/dev/mgtr')
    mqttc.on_message = on_message

    it = input_thread(mqttc, topic)
    it.start()
    mqttc.loop_forever()
