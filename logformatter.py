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
