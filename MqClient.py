import mosquitto
import sys


class MqttClient:
    def __init__(self, servIp='', servPort=1883, logHandle=sys.stdout):
        self.mqttPort = int(servPort)
        self.mqttServIp = str(servIp)
        self.log = logHandle
        self.client = mosquitto.Mosquitto()

    def connect(self):
        self.client.connect(self.mqttServIp, self.mqttPort)
        self.client.loop()
