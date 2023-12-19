#!/usr/bin/python3

import subprocess
import logformatter
import logger


def run(command):
    success = True
    report_url = None
    try:
        with open("perfecto-gradle-wrapper.log", "a") as write_handle:
            log = logger.Log(write_handle)
            log.message("Executing command: \x1b[38;5;115m%s\x1b[0m" % command)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            for line in process.stdout:
                line = line.decode()
                if line == "\n" or line == "":
                    continue
                if "reporting.perfectomobile" in line:
                    report_url = line
                    # line = logformatter.fix_reporting_url(line)
                if "Your management id is" in line:
                    line = logformatter.fix_coloring(line)
                log.message(line)
    except Exception as ex:
        log.message(ex)
        success = False

    return {"success": success, "reportUrl": report_url}
