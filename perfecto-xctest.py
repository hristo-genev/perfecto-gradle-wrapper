#!/usr/bin/python3

import sys
import cmdparser
import subprocess
import webbrowser
from datetime import datetime
from gradle_helper import get_gralde_exe

print("")
print("##################################################")
print("####    PERFECTO ESPRESSO/XCUITEST WRAPPER   #####")
print("##################################################")
print("")
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
#os.system(command)

report_url=None
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
with open("latest-xcuitest.log", "w") as w:
    for line in process.stdout:
        line = line.decode().replace("\n", "")
        if line == "\n" or line == "":
            continue
        if "reporting.perfectomobile" in line:
            line = line\
                .replace("reporting.perfectomobile", "app.perfectomobile")\
                .replace("[", "%5B")\
                .replace("]", "%5D")
            report_url = line
        print(line)

        line = line.replace("\x1b[33m", "")\
            .replace("\x1b[38;5;244m", "")\
            .replace("\x1b[38;5;115m", "")\
            .replace("\x1b[38;5;175m", "")\
            .replace("\x1b[38;5;240m", "")\
            .replace("\x1b[0m", "")
        w.write("%s\n" % line)

print("Finished execution at %s" % datetime.now())
webbrowser.open(report_url)
