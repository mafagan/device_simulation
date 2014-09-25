
class app:
    def __init__(self, name):
        self.name = name
        self.status = 'paused'

    def start(self):
        self.status = 'running'

    def stop(self):
        self.status = 'paused'

    def setStatus(self, status):
        self.status = status
