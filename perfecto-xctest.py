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

virtual_devices_appendix = "-vd" if cmdparser.is_vd_command else ""
command = "%s perfecto-xctest%s %s" % (gradle_exe, virtual_devices_appendix, cmd)
print("Executing command:\n%s" % command)
os.system(command)
print("Finished execution at %s" % datetime.now())
