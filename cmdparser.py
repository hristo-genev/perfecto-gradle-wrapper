import sys
import json
import getopt
import tokenstorage as tokens

is_vd_command = False
is_espresso = False
is_xcuitest = False


def parse_args():
    opts = []
    args = []
    try:
        print(sys.argv[1:])
        opts, args = getopt.getopt(
            sys.argv[1:],
            "ha:f:i:c:m:d:t:P:v:n:",
            ["authFilePath=", "cloud=", "configFileLocation=", "itmsServerUrl=", "testClassNames=", "testMethodNames=",
             "device=", "securityToken=", "vd", "noincrement", "debug", "stacktrace"])
        return opts, args
    except getopt.GetoptError as er:
        print('Wrong arguments provided. Exiting.')
        print(er)
        return opts, args


def load_gradle_config(config_file):
    try:
        return json.load(open(config_file))
    except FileNotFoundError as er:
        print("ERROR Config file '%s' not found" % config_file)
    except json.JSONDecodeError as er:
        print("ERROR Config file does not contain valid JSON. %s" % er)
    except Exception as ex:
        print("ERROR %s " % ex)
    return None


def get_command():
    cloud = None
    command_template = ""
    config_file = "configFile.json"
    token = None
    device_names = []
    auto_increment_job_number = True

    print("Arguments: %s" % sys.argv)
    opts, args = parse_args()
    if not opts:
        print("Invalid arguments provided!")
        sys.exit()
    for opt, arg in opts:

        if opt == '-h':
            print("Help yourself!")
            sys.exit()

        elif opt in ("-c", "--cloud"):
            cloud = arg
            hostname = cloud if cloud.endswith(".perfectomobile.com") else cloud + ".perfectomobile.com"
            command_template += " -PcloudURL=\"%s\"" % hostname
            print("Overwriting cloud name \x1b[38;5;115m%s\x1b[0m" % cloud)

        elif opt in ("-f", "--configFileLocation"):
            config_file = arg
            command_template += " -PconfigFileLocation=\"%s\"" % config_file
            print("Overwriting config file name \x1b[38;5;115m%s\x1b[0m" % config_file)

        elif opt in ("-i", "--itmsServerUrl"):
            if arg != "https://test-executor.perfectomobile.com":
                command_template += " -PitmsServerUrl=\"%s\"" % arg
            print("Using none-default server: \x1b[38;5;115m%s\x1b[0m" % arg)

        elif opt in ("-a", "--authFilePath"):
            auth_file_path = arg
            print("Using custom token storage file: \x1b[38;5;115m%s\x1b[0m" % auth_file_path)

        elif opt in ("-t", "--securityToken"):
            token = arg
            command_template += "-PsecurityToken =\"%s\"" % token
            print("Overwriting token: %s" % token)

        elif opt in ("-c", "--testClassNames"):
            command_template += " -PtestClassNames=\"%s\"" % arg
            print("Overwriting testClassNames: \x1b[38;5;115m%s\x1b[0m" % arg)

        elif opt in ("-m", "--testMethodNames"):
            command_template += " -PtestMethodNames=\"%s\"" % arg
            print("Overwriting testMethodNames: \x1b[38;5;115m%s\x1b[0m" % arg)

        elif opt in ("-n", "--noincrement"):
            auto_increment_job_number = False
            print("Disabling auto_increment_job_number")

        elif opt in ("-d", "--device"):
            print("Overwriting device id: \x1b[38;5;115m%s\x1b[0m" % arg)
            device_names.append(arg)

        elif opt in "--debug":
            command_template += " --debug"
            print("Enabled debug")

        elif opt in ("-s", "--stacktrace"):
            print("Enabled stacktrace")
            command_template += " --stacktrace"

        elif opt.startswith('-P'):
            print("Adding generic argument \x1b[38;5;115m%s\x1b[0m" % arg)
            command_template += " -P%s" % arg

        elif opt in ("-v", "--vd"):
            global is_vd_command
            is_vd_command = True
            print("Running on virtual devices")

    gradle_config = load_gradle_config(config_file)
    if not gradle_config:
        sys.exit()

    cloud = cloud if cloud else gradle_config["cloudURL"].replace('.perfectomobile.com', '')
    if not cloud:
        print("No cloud name specified. Please use the -c parameter")
        sys.exit()

    # If token is not set via cmd argument, look in the config
    # if not found, look in the token storage file
    token = token if token else gradle_config.get("securityToken", None)
    if not token:
        token = tokens.get_token_for_cloud(cloud)
        if not token:
            sys.exit()

    command_template += " -PsecurityToken=\"%s\"" % token

    global is_xcuitest
    global is_espresso
    is_xcuitest = gradle_config["appPath"].endswith("ipa")
    is_espresso = not is_xcuitest

    if len(device_names) > 0:
        print("Adding devices to config file")
        gradle_config["devices"] = []
        for device in device_names:
            gradle_config["devices"].append({"deviceName": device})

        with open(config_file, "w") as f:
            print("Saving config modifications")
            f.write(json.dumps(gradle_config, indent=2))

    if auto_increment_job_number:
        job_number = gradle_config.get("jobNumber", -1)
        if job_number > 0:
            job_number = job_number + 1
            gradle_config["jobNumber"] = job_number
            with open(config_file, "w") as f:
                print("Saving incremented jobNumber \x1b[38;5;115m%s\x1b[0m" % job_number)
                f.write(json.dumps(gradle_config, indent=2))

    return command_template
