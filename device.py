#!/usr/bin/python
import macro
import app
import random
import sys
import os

# Class to simulate device and excute command


class device:
    def __init__(self, projID, devID):
        self.devId = devID
        self.projID = projID
        self.ver = 'v1.0'
        self.cfg = None
        self.applist = {}
        self.files = []

        self.cmd_list = {
            macro.cmd_list['getver']: self.handle_getver,
            macro.cmd_list['getapplist']: self.handle_getapplist,
            macro.cmd_list['getcfg']: self.handle_getcfg,
            macro.cmd_list['setcfg']: self.handle_setcfg,
            macro.cmd_list['ping']: self.handle_ping,
            macro.cmd_list['updatefirmware']: self.handle_updatefirmware,
            macro.cmd_list['system']: self.handle_system,
            macro.cmd_list['startapp']: self.handle_startapp,
            macro.cmd_list['stopapp']: self.handle_stopapp,
            macro.cmd_list['installapp']: self.handle_installapp,
            macro.cmd_list['reboot']: self.handle_reboot,
            macro.cmd_list['filec2d']: self.handle_filec2d,
            macro.cmd_list['filed2c']: self.handle_filed2c,
            macro.cmd_list['rpccall']: self.handle_rpccall,
        }

    def set_ver(self, ver):
        self.ver = ver

    def add_app(self, appname, status):
        self.applist[appname] = app.app(appname)
        self.applist[appname].setStatus(status)

    def set_cfg(self, cfg):
        self.cfg = cfg

    def cmd_exec(self, cmd, args):
        res = self.cmd_list[macro.cmd_list[cmd]](args)
        return res

# return value: [status_code, argc, argv...]

    def handle_getver(self, args):
        rand_num = random.randint(1, 100)
        if rand_num <= macro.cmd_fail_percent[macro.GETVER]:
            return None

        res = []

        res.append(0)
        res.append(1)
        res.append(self.ver)

        return res

    def handle_getapplist(self, args):
        rand_num = random.randint(1, 100)
        if rand_num <= macro.cmd_fail_percent[macro.GETAPPLIST]:
            return None

        res = []

        res.append(0)
        res.append(len(self.applist))

        for app_itm in self.applist.keys():
            ret_value = ''
            ret_value = ret_value + app_itm + ',' \
                + self.applist[app_itm].status + '\r\n'
            res.append(ret_value)
        return res

    def handle_getcfg(self, args):
        rand_num = random.randint(1, 100)

        if rand_num <= macro.cmd_fail_percent[macro.GETCFG]:
            return None

        res = []
        res.append(0)
        res.append(1)
        res.append(self.cfg)
        return res

    def handle_setcfg(self, args):
        rand_num = random.randint(1, 100)

        if rand_num <= macro.cmd_fail_percent[macro.SETCFG]:
            return None

        if len(args) < 2:
            return None

        self.cfg = args[1]
        res = []
        res.append(0)
        res.append(0)
        return res

    def handle_ping(self, args):
        rand_num = random.randint(1, 100)

        if rand_num <= macro.cmd_fail_percent[macro.PING]:
            return None

        res = []
        res.append(0)
        res.append(1)
        res.append('pong\r\n')
        return res

    def handle_startapp(self, args):
        rand_num = random.randint(1, 100)

        if rand_num <= macro.cmd_fail_percent[macro.STARTAPP]:
            return None

        if len(args) < 2:
            return None

        appname = args[1]

        res = []
        if appname in self.applist:
            self.applist[appname].start()
            res.append(0)
            res.append(0)
        else:
            res.append(-1)
            res.append(0)

        return res

    def handle_stopapp(self, args):
        rand_num = random.randint(1, 100)

        if rand_num <= macro.cmd_fail_percent[macro.STOPAPP]:
            return None

        if len(args) < 2:
            return None

        appname = args[1]

        res = []
        if appname in self.applist:
            self.applist[appname].stop()
            res.append(0)
            res.append(0)
        else:
            res.append(-1)
            res.append(0)

        return res

    def handle_system(self, args):
        rand_num = random.randint(1, 100)

        if rand_num <= macro.cmd_fail_percent[macro.SYSTEM]:
            return None

        pass

    def handle_reboot(self, args):
        rand_num = random.randint(1, 100)

        if rand_num <= macro.cmd_fail_percent[macro.REBOOT]:
            return None

        res = []
        res.append(0)
        res.append(0)
        return res

    def handle_updatefirmware(self, args):
        rand_num = random.randint(1, 100)

        if rand_num <= macro.cmd_fail_percent[macro.UPDATEFM]:
            return None

        res = []
        res.append(0)
        res.append(0)

        return res

    def handle_installapp(self, args):
        rand_num = random.randint(1, 100)

        if rand_num <= macro.cmd_fail_percent[macro.INSTALLAPP]:
            return None

        if args[0] != 1:
            return None

        if len(args) < 2:
            return None

        if not (args[1] in self.applist):
            self.applist[args[1]] = app.app(args[1])
        res = []
        res.append(0)
        res.append(0)
        return res

    def handle_filec2d(self, args):
        rand_num = random.randint(1, 100)
        if rand_num <= macro.cmd_fail_percent[macro.FILEC2D]:
            return None

        if len(args) != 4:
            return None
        path = args[1].strip()
        filedata = args[3][:-1]

        filepath = sys.path[0] + '/filesystem/' + self.projID + '/' \
            + self.devId + path

        dirpath = os.path.dirname(filepath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        f = file(filepath, 'wb')
        f.write(filedata)
        f.close()

        res = []
        res.append(0)
        res.append(0)
        return res

    def handle_filed2c(self, args):
        rand_num = random.randint(1, 100)

        if rand_num <= macro.cmd_fail_percent[macro.FILED2C]:
            return None

        if len(args) != 2:
            return None

        path = sys.path[0] + '/filesystem/' + self.projID + '/' + self.devId \
            + args[1]
        if os.path.isfile(path):
            filesize = os.path.getsize(path)
            f = file(path, "rb")
            filedata = f.read()
            f.close()

            res = []
            res.append(0)
            res.append(1)
            res.append('\\xB'+str(filesize)+'\r\n')
            res.append(filedata+'\r\n')
            return res
        else:
            return None

    def handle_rpccall(self, args):
        rand_num = random.randint(1, 100)

        if rand_num <= macro.cmd_fail_percent[macro.RPCCALL]:
            return None

        return None
