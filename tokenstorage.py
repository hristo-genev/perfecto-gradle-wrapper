import json
import config


def get_token_for_cloud(cloud_name):
    """
    Reads token from token storage file and returns it.
    :param cloud_name: The name of the cloud we want to authenticate to
    :return: The security token, False if not found
    """
    try:
        print ("Using token storage file: %s" % config.auth_file_path)
        token = json.load(open(config.auth_file_path))["tokens"][cloud_name]
        print("Found token for %s" % cloud_name)
        return token

    except FileNotFoundError:
        print("ERROR Tokens file %s not found!" % config.auth_file_path)

    except KeyError:
        print("ERROR Token not found for %s" % cloud_name)

    except json.JSONDecodeError as er:
        print("ERROR when reading tokens file %s" % er)

    except Exception as er:
        print("ERROR %s" % er)

    return False
