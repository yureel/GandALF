import sys


class Logger(object):
    def __init__(self, nameFlowsheet):
        self.terminal = sys.stdout
        self.log = open(nameFlowsheet+"/logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
