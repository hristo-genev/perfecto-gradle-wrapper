import os
import sys

def get_gralde_exe():
    '''
    Returns gradle executable
    :return:
    '''
    gradle_home = os.getenv("GRADLE_USER_HOME")
    if gradle_home is None:
        return None

    return os.path.join(gradle_home, "bin", "gradle")