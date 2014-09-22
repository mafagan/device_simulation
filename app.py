import macro


class app:
    def __init__(self, name):
        self.name = name
        self.status = macro.PAUSED

    def start(self):
        self.status = macro.RUNNING

    def stop(self):
        self.status = macro.PAUSED
