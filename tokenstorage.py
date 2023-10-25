import json
import config
import configparser

def get_token_for_cloud(cloud_name):
    """
    Reads token from token storage file and returns it.
    :param cloud_name: The name of the cloud we want to authenticate to
    :return: The security token, False if not found
    """
    token = None

    try:
        print("Using token storage file: %s" % config.auth_file_path)
        if config.auth_file_path.endswith(".json"):
            token = json.load(open(config.auth_file_path))["tokens"][cloud_name]
        elif config.auth_file_path.endswith(".ini"):
            tokens_storage = configparser.ConfigParser()
            tokens_storage.read(config.auth_file_path)
            token = tokens_storage['tokens'][cloud_name]
        else:
            print("Not supported token storage file format (must be .ini or .json)")

    except FileNotFoundError:
        print("ERROR Tokens file %s not found!" % config.auth_file_path)

    except KeyError:
        print("ERROR Token not found for %s" % cloud_name)

    except json.JSONDecodeError as er:
        print("ERROR when reading tokens file %s" % er)

    except Exception as er:
        print("ERROR %s" % er)

    if token:
        print("Found token for %s" % cloud_name)
    else:
        print("Token not found for cloud %s" % cloud_name)
    return token


def get_token_from_ini_file(ini_file, cloud_name):
    """
    Reads token from token storage file and returns it.
    :param ini_file: The path to the ini file
    :return: The security token, False if not found
    """
    content = []
    with open(ini_file, "r") as f:
        content = f.readlines()

    for l in content:
        if l.strip().startswith(cloud_name):
            return l.split("=")[1]

    return False
