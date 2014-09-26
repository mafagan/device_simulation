#!/usr/bin/python
import time

# Task to excute


class task:
    def __init__(self):
        self.flag = True

    def setSerNumber(self, serNumber):
        self.serNumber = serNumber

    def setProjID(self, projID):
        self.projID = projID

    def setDevice(self, device):
        self.device = device

    def setOperation(self, operation):
        self.operation = operation

    def setDelay(self, delay):
        self.endtime = time.time() + delay/1000.0

    def setArgs(self, args):
        self.args = args

    def setValidFlag(self, flag=True):
        self.flag = flag
