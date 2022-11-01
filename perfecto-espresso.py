import os
import sys
import config
import cmdparser
from datetime import datetime

print("Starting execution at %s" % datetime.now())
cmd = cmdparser.get_command()
if not cmd:
    sys.exit()

command = "gradle perfecto-android-inst %s" % cmd
print("Executing command:\n%s" % command)
os.system(command)
print("Finished execution at %s" % datetime.now())
