#!/usr/bin/python3

import sys
import cmdparser
import subprocess
import webbrowser
from datetime import datetime
from gradle_helper import get_gralde_exe
# from executor import run
import executor

print("")
print("##################################################")
print("####    PERFECTO ESPRESSO/XCUITEST WRAPPER   #####")
print("##################################################")
print("")
command_arguments = cmdparser.get_command()
if not command_arguments:
    print("No arguments provided")
    sys.exit()

if not cmdparser.is_xcuitest:
    print("Running espresso test but no espresso config found!")
    sys.exit()

gradle_exe = get_gralde_exe()
if gradle_exe is None:
    print("\033[0;31mNo gradle found. Please add a GRADLE_USER_HOME variable pointing to Gradle's folder\x1b[0m")
    sys.exit()

virtual_devices_appendix = "-vd" if cmdparser.is_vd_command else ""
command = "%s perfecto-xctest%s %s" % (gradle_exe, virtual_devices_appendix, cmd)

result = executor.run(command)

print("Opening report URL in default browser: %s" % result["reportUrl"])
if result["reportUrl"]:
    webbrowser.open(result["reportUrl"])

