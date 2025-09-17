import re


def fix_reporting_url(line):
    if not line:
        return
    if "reporting.perfectomobile" in line:
        line = line \
            .replace("reporting.perfectomobile", "app.perfectomobile") \
            .replace("[", "%5B") \
            .replace("]", "%5D")
        return line


# #\x1b[38;5;115m \x1b[0m
# \x1b[38;5;240m \x1b[0m
#

def remove_coloring(line):
    if not line:
        return
    line = line.replace("\x1b[33m", "") \
        .replace("\x1b[38;5;244m", "") \
        .replace("\x1b[38;5;115m", "") \
        .replace("\x1b[38;5;175m", "") \
        .replace("\x1b[38;5;240m", "") \
        .replace("\x1b[0m", "")
    return line


def fix_coloring(line):
    # if "\x1b[38;5;244m" in line and not line.endswith("\x1b[0m"):
    #     line = line + "\x1b[0m"
    if "Your management id is" in line:
        line = line.replace("Your management id is: ", "")
        line = "Your management id is: \x1b[38;5;115m%s\x1b[0m" % line
    return line


def add_test_numbering(line, test_numbering):
    #Device: R5CX23DF8FN Samsung Galaxy S24 Ultra: TestResult{className: com.singaporeair.base.login.BaseLoginFragmentTest, methodName: onClicksAvatar_givenLoginSuccessAndNoGraceFlow_givenLslAccessTokenExpired_callsRefreshTokenWithServerError_seesAvatarBlue, status
    device_id = re.compile("Device\:\s*(.*?)\s").findall(line)[0]
    if not test_numbering.get(device_id):
        test_numbering[device_id] = 1
    current_test_number = test_numbering.get(device_id)
    test_numbering[device_id] += 1

    class_matches = re.compile("TestResult\{className\:\s*(.*?)\,").findall(line)
    if len(class_matches) > 0:
        method_matches = re.compile("methodName\:\s*(.*?)\,").findall(line)
        if len(method_matches) > 0:
            test_name = "%s#%s" % (class_matches[0], method_matches[0])
            status_matches = re.compile("status\:\s*(.*?)}").findall(line)
            return re.sub(r"TestResult.*\}", "%s. %s -> %s" % (current_test_number, test_name, status_matches[0]), line)

    return line
