#!/usr/bin/python3

import sys
import cmdparser
import webbrowser
import executor
from gradle_helper import get_gralde_exe

command_arguments = cmdparser.get_command()
if not command_arguments or not cmdparser.is_espresso:
    sys.exit()

gradle_exe = get_gralde_exe()
if gradle_exe is None:
    print("\033[0;31mNo gradle found. Please add a GRADLE_USER_HOME variable pointing to Gradle's folder\x1b[0m")
    sys.exit()

virtual_devices_appendix = "-vd" if cmdparser.is_vd_command else ""
command = "%s perfecto-android-inst%s %s" % (gradle_exe, virtual_devices_appendix, command_arguments)

result = executor.run(command)

print("Opening report URL in default browser: %s" % result["reportUrl"])
if result["reportUrl"]:
    webbrowser.open(result["reportUrl"])
