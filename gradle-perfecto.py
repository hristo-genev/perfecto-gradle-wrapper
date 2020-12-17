import os
import sys
import json
import getopt

task = ""
cloud = ""
hostname = ""
configFile = "configFile.json"
itmsServerUrl = "test-executor"
authFilePath = "c:\\Users\\hristo\\securityTokens.json"
token = ""
testMethodNames = ""
testClassNames = ""
debug = False
deviceNames = []
config = {}
originalConfig = {}
commandTemplate = "gradle.bat %s -PcloudURL=\"%s\" -PsecurityToken=\"%s\"" 
commandArguments = ()

print ("Arguments: %s" % sys.argv)

# Mandatory arguments
if len(sys.argv) < 2:
    print ("No task name provided. Use android or perfecto-android-inst or ios or perfecto-xctest")
    sys.exit(2)
if len(sys.argv) < 3:
    print ("No cloud name provided.")
    sys.exit(2)
else:
    if sys.argv[1].lower() == 'android-inst' or sys.argv[1].lower() == 'xctest' or sys.argv[1].lower() == 'perfecto-android-inst' or sys.argv[1].lower() == 'perfecto-xctest':
        task = 'perfecto-android-inst' if 'android' in sys.argv[1].lower()  else 'perfecto-xctest'
        print ("Running task %s" % task)
    else:
        print ("No valid task provided: '%s'. Use 'android-inst' or 'xctest'" % sys.argv[1].lower())
        sys.exit(2)

cloud = sys.argv[2].lower()
hostname = cloud if cloud.endswith(".perfectomobile.com") else cloud + ".perfectomobile.com"
commandArguments = (task, hostname)

# if token was not overwritten
print ("token %s" % token)
try:
    token = json.load(open(authFilePath))["tokens"][cloud]       
    print ("Found token for %s" % cloud)
    commandArguments += (token,)
except KeyError:
    print ("Token not found for %s" % cloud)


# Optional arguments
try:
    print (sys.argv[3:])
    opts, args = getopt.getopt(sys.argv[3:], "ha:f:i:c:m:t:d:", 
        ["--authFilePath=", "--configFileLocation=", "--itmsServerUrl=", "--testClassNames=", "--testMethodNames=", "--securityToken=", "--deviceNames="])

except getopt.GetoptError:
    print ('Wrong arguments provided. Exiting.')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print ("Help yourself!")
        sys.exit()
    elif opt in ("-f", "--configFileLocation"):
        configFile = arg
    elif opt in ("-i", "--itmsServerUrl"):
        itmsServerUrl = arg
        print ("Using none-default server: %s" % itmsServerUrl)
    elif opt in ("-a", "--authFilePath"):
        authFilePath = arg
        print ("Using custom token storage file: %s" % authFilePath)               
    elif opt in ("-t", "--securityToken"):
        token = arg
        print ("Overwriting token: %s" % token)
    elif opt in ("-c", "--testClassNames"):
        testClassNames = arg
        print ("Overwriting testClassNames: %s" % testClassNames)
    elif opt in ("-m", "--testMethodNames"):
        testMethodNames = arg
        commandTemplate += " -PtestMethodNames=\"%s\""
        commandArguments += (arg,)
        print ("Overwriting testMethodNames: %s" % testMethodNames)
    elif opt in ("-d", "--debug"):
        debug = True
        print ("Overwriting debug: True")        
    elif opt in ("--deviceNames"):
        devices = arg.split(";")
        print ("Overwriting deviceNames: %s" % devices)    


itmsServerUrl = itmsServerUrl if itmsServerUrl.endswith(".perfectomobile.com") else itmsServerUrl + ".perfectomobile.com"
itmsServerUrl = "https://%s" % itmsServerUrl

print ("Running on cloud %s" % hostname)
print ("Using config file %s" % configFile)


if len(deviceNames) > 0:
    print ("Adding deviceNames to config file")
    with open(configFile, "r+") as f:
        config = json.load(f.read())
        originalConfig = config
        config["devices"] = []
        for deviceName in deviceNames:
            config["devices"].append({"devicename": deviceName})
        
        print ("Saving config modifications")
        f.write()



command = "gradle.bat %s -PcloudURL=\"%s\" -PsecurityToken=\"%s\"" % (task, hostname, token)
print (commandTemplate)
print (commandArguments)
command = commandTemplate % commandArguments

if configFile != "configFile.json":
    command += " -PconfigFileLocation=\"%s\""

if itmsServerUrl != "https://test-executor.perfectomobile.com":
    command += " -PitmsServerUrl=\"%s\"" % itmsServerUrl



print ("Executing command:\n%s\n" % command)

os.system(command)

if len(deviceNames) > 0:
    with open(configFile, "w") as w:
        print ("Restoring original config file %s" % configFile)
        json.dump(config, w, indent=4)