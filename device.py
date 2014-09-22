import macro


class device:
    def __init__(self, projID, devID):
        self.devId = devID
        self.projID = projID
        self.ver = 'v1.0'
        self.cfg = {}
        self.applist = {}
        self.files = []

        self.cmd_list = {
            macro.cmd[macro.GETVER]: self.handle_getver,
            macro.cmd[macro.GETAPILIST]: self.getapilist,
            macro.cmd[macro.GETAPPLIST]: self.getapplist,
            macro.cmd[macro.GETCFG]: self.handle_getcfg,
            macro.cmd[macro.SETCFG]: self.handle_setcfg,
            macro.cmd[macro.PING]: self.handle_ping,
            macro.cmd[macro.UPDATEFM]: self.handle_updatefirmware,
            macro.cmd[macro.SYSTEM]: self.handle_system,
            macro.cmd[macro.STARTAPP]: self.handle_startapp,
            macro.cmd[macro.STOPAPP]: self.handle_stopapp,
            macro.cmd[macro.INSTALLAPP]: self.handle_installapp,
            macro.cmd[macro.REBOOT]: self.handle_reboot,
            macro.cmd[macro.FILEC2D]: self.handle_filec2d,
            macro.cmd[macro.FILED2C]: self.handle_filed2c,
            macro.cmd[macro.RPCCALL]: self.handle_rpccall,
        }

    def cmd_exec(self, cmd, args):
        self.cmd_list[cmd](args)

    def handle_getver(self, args):
        pass

    def handle_getapplist(self, args):
        pass

    def handle_getapilist(self, args):
        pass

    def handle_getcfg(self, args):
        pass

    def handle_setcfg(self, args):
        pass

    def handle_ping(self, args):
        pass

    def handle_startapp(self, args):
        appname = args[0]

        if appname in self.applist:
            pass
        else:
            pass

    def handle_stopapp(self, args):
        pass

    def handle_system(self, args):
        pass

    def handle_reboot(self, args):
        pass

    def handle_updatefirmware(self, args):
        pass

    def handle_installapp(self, args):
        pass

    def handle_filec2d(self, args):
        pass

    def handle_filed2c(self, args):
        pass

    def handle_rpccall(self, args):
        pass

if __name__ == '__main__':
    devc = device()
    devc.cmd_exec('getver')
