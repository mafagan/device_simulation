import macro
import app


class device:
    def __init__(self, projID, devID):
        self.devId = devID
        self.projID = projID
        self.ver = 'v1.0'
        self.cfg = None
        self.applist = {}
        self.files = []

        self.cmd_list = {
            macro.cmd['getver']: self.handle_getver,
            macro.cmd['getapilist']: self.getapilist,
            macro.cmd['getapplist']: self.getapplist,
            macro.cmd['getcfg']: self.handle_getcfg,
            macro.cmd['setcfg']: self.handle_setcfg,
            macro.cmd['ping']: self.handle_ping,
            macro.cmd['updatefirmware']: self.handle_updatefirmware,
            macro.cmd['system']: self.handle_system,
            macro.cmd['startapp']: self.handle_startapp,
            macro.cmd['stopapp']: self.handle_stopapp,
            macro.cmd['installapp']: self.handle_installapp,
            macro.cmd['reboot']: self.handle_reboot,
            macro.cmd['filec2d']: self.handle_filec2d,
            macro.cmd['filed2c']: self.handle_filed2c,
            macro.cmd['rpccall']: self.handle_rpccall,
        }

    def cmd_exec(self, cmd, args):
        self.cmd_list[cmd](args)

# return value: [status_code, argc, argv...]
#
    def handle_getver(self, args):
        res = []

        res.append(0)
        res.append(1)
        res.append(self.ver)

        return res

    def handle_getapplist(self, args):
        res = []

        res.append(0)
        res.append(len(self.applist))

        for app_itm in self.applist:
            ret_value = ''
            ret_value = ret_value + app_itm + ',' \
                + self.applist[app_itm].status + '\r\n'
            res.append(ret_value)
        return res

    def handle_getapilist(self, args):
        pass

    def handle_getcfg(self, args):

        res = []
        res.append(0)
        res.append(1)
        res.append(self.cfg)
        return res

    def handle_setcfg(self, args):

        self.cfg = args[1]
        res = []
        res.append(0)
        res.append(0)
        return res

    def handle_ping(self, args):

        res = []
        res.append(0)
        res.append(1)
        res.append('pong\r\n')
        return res

    def handle_startapp(self, args):
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
        pass

    def handle_reboot(self, args):
        pass

    def handle_updatefirmware(self, args):
        res = []
        res.append(0)
        res.append(0)

        return res

    def handle_installapp(self, args):
        if args[0] != 1:
            return None

        if not (args[1] in self.applist):
            self.applist[args[1]] = app.app(args[1])
        res = []
        res.append(0)
        res.append(0)
        return res

    def handle_filec2d(self, args):
        pass

    def handle_filed2c(self, args):
        pass

    def handle_rpccall(self, args):
        pass

if __name__ == '__main__':
    devc = device()
    devc.cmd_exec('getver')
