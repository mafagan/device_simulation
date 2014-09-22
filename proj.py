import device


class proj:
    def __init__(self, projID):
        self.projID = projID
        self.devSet = {}

    def addDevice(self, devName):
        if devName in self.devSet:
            pass
        else:
            self.devSet[devName] = device(self.projID, devName)
