import logformatter
from datetime import datetime


class Log:
    def __init__(self, file_handle):
        self.file_handle = file_handle

    def message(self, line):
        line = "%s | %s" % (datetime.now(), line.replace("\n", ""))
        print(line)
        line = logformatter.remove_coloring(line)
        self.file_handle.write("%s\n" % line)
