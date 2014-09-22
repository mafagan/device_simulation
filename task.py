import time


class task:
    def __init__(self):
        pass

    def setSerNumber(self, serNumber):
        self.serNumber = serNumber

    def setProjID(self, projID):
        self.projID = projID

    def setDevice(self, device):
        self.device = device

    def setOperation(self, operation):
        self.operation = operation

    def setDelay(self, delay):
        self.endtime = (int)(time.time() + delay)

    def setArgs(self, args):
        self.args = args
