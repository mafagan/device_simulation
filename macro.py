#!/usr/bin/python
GETVER = 1
GETAPPLIST = 2
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

deviation = 150
conf_file = 'sim.conf'
# MQTT Broker config
MQTT_BROKER_HOST = '127.0.0.1'
MQTT_BROKER_PORT = 1883

cmd = {
    GETVER: 'getver',
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

cmd_list = {
    'getver': GETVER,
    'getapplist': GETAPPLIST,
    'getcfg': GETCFG,
    'setcfg': SETCFG,
    'ping': PING,
    'startapp': STARTAPP,
    'stopapp': STOPAPP,
    'system': SYSTEM,
    'reboot': REBOOT,
    'updatefirmware': UPDATEFM,
    'installapp': INSTALLAPP,
    'filec2d': FILEC2D,
    'filed2c': FILED2C,
    'rpccall': RPCCALL

}

# Delay config
cmd_delay = {}

# Device offline probablity config
cmd_fail_percent = {}
