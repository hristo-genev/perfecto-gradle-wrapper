#!/usr/bin/python3

import subprocess
import logformatter
import logger


def run(command):
    success = True
    report_url = None
    should_retry = False

    with open("perfecto-gradle-wrapper.log", "a") as write_handle:
        try:
            log = logger.Log(write_handle)
            log.message("Executing command: \x1b[38;5;115m%s\x1b[0m" % command)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            test_numbering = {}
            for line in process.stdout:
                line = line.decode()
                if line == "\n" or line == "":
                    continue
                if "reporting.perfectomobile" in line or "app.perfectomobile" in line:
                    report_url = line.replace("Report url: ", "")
                    # line = logformatter.fix_reporting_url(line)
                if "Your management id is" in line:
                    line = logformatter.fix_coloring(line)

                if "TestResult{className:" in line:
                    line = logformatter.add_test_numbering(line, test_numbering)
                log.message(line)
                if "Task perfecto failed with message: I/O error on PUT request" in line:
                    should_retry = True

        except KeyboardInterrupt:
            log.message("Keyboard interrupted! Stopping execution!")
            success = False
        except Exception as ex:
            log.message(ex)
            success = False

    return {"success": success, "reportUrl": report_url, "retry": should_retry}
