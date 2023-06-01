#!/usr/bin/python3

import os
import sys
import cmdparser
from datetime import datetime
from gradle_helper import get_gralde_exe

print("Starting execution at %s" % datetime.now())
cmd = cmdparser.get_command()
if not cmd:
    sys.exit()

gradle_exe = get_gralde_exe()
if gradle_exe is None:
    print("No gradle found. Please add a GRADLE_USER_HOME variable pointing to Gradle's folder")
    sys.exit()

command = "%s perfecto-android-inst %s" % (gradle_exe, cmd)
print("Executing command:\n%s" % command)
os.system(command)
print("Finished execution at %s" % datetime.now())
