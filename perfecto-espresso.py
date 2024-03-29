#!/usr/bin/python3

import sys
import cmdparser
import webbrowser
import executor
from gradle_helper import get_gralde_exe

print("")
print("##################################################")
print("####    PERFECTO ESPRESSO WRAPPER   #####")
print("##################################################")
print("")
command_arguments = cmdparser.get_command()
if not command_arguments:
    print("No arguments provided")
    sys.exit()

if not cmdparser.is_espresso:
    print("Running espresso test but no espresso config found!")
    sys.exit()

gradle_exe = get_gralde_exe()
if gradle_exe is None:
    print("\033[0;31mNo gradle found. Please add a GRADLE_USER_HOME variable pointing to Gradle's folder\x1b[0m")
    sys.exit()

virtual_devices_appendix = "-vd" if cmdparser.is_vd_command else ""
command = "%s perfecto-android-inst%s %s" % (gradle_exe, virtual_devices_appendix, command_arguments)

result = executor.run(command)

print("Report URL: %s" % result["reportUrl"])
if result["success"] and result["reportUrl"]:
    webbrowser.open(result["reportUrl"])

