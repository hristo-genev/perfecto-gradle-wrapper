#!/usr/bin/python3

import sys
import cmdparser
import subprocess
import webbrowser
from gradle_helper import get_gralde_exe
import executor

print("")
print("##################################################")
print("####    PERFECTO XCUITEST WRAPPER   #####")
print("##################################################")
print("")
command_arguments = cmdparser.get_command()
if not command_arguments:
    print("No arguments provided")
    sys.exit()

if not cmdparser.is_xcuitest:
    print("Running xcuitest but no xcuitest config found!")
    sys.exit()

gradle_exe = get_gralde_exe()
if gradle_exe is None:
    print("\033[0;31mNo gradle found. Please add a GRADLE_USER_HOME variable pointing to Gradle's folder\x1b[0m")
    sys.exit()

virtual_devices_appendix = "-vd" if cmdparser.is_vd_command else ""
command = "%s perfecto-xctest%s %s" % (gradle_exe, virtual_devices_appendix, command_arguments)

result = executor.run(command)
if result["retry"]:
    print("Running again due to possible error in previous attempt")
    result = executor.run(command)

print("Report URL: %s" % result["reportUrl"])
if result["success"] and result["reportUrl"]:
    webbrowser.open(result["reportUrl"])

