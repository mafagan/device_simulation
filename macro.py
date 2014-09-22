
GETVER = 1
GETAPPLIST = 2
GETAPILIST = 3
GETCFG = 4
SETCFG = 5
PING = 6
STARTAPP = 7
STOPAPP = 8
SYSTEM = 9
REBOOT = 10
UPDATEFM = 11
INSTALLAPP = 12
FILEC2D = 13
FILED2C = 14
RPCCALL = 15


RUNNING = 1
PAUSED = 2

MQTT_BROKER_IP = '127.0.0.1'
MQTT_BROKER_PORT = 1883

cmd = {
    GETVER: 'getver',
    GETAPILIST: 'getapilist',
    GETAPPLIST: 'getapplist',
    GETCFG: 'getcfg',
    SETCFG: 'setcfg',
    PING: 'ping',
    STARTAPP: 'startapp',
    STOPAPP: 'stopapp',
    SYSTEM: 'system',
    REBOOT: 'reboot',
    UPDATEFM: 'updatefirmware',
    INSTALLAPP: 'installapp',
    FILEC2D: 'filec2d',
    FILED2C: 'filed2c',
    RPCCALL: 'rpccall'
}

cmd_delay = {
    GETVER: [100, 200],
    GETCFG: [100, 200],
    GETAPILIST: [100, 200],
    GETAPPLIST: [100, 200],
    SETCFG: [100, 500],
    PING: [100, 500],
    STARTAPP: [100, 500],
    STOPAPP: [100, 500],
    SYSTEM: [100, 500],
    REBOOT: [100, 500],
    UPDATEFM: [100, 500],
    INSTALLAPP: [100, 500],
    FILEC2D: [100, 500],
    FILED2C: [100, 500],
    RPCCALL: [100, 500]
}
