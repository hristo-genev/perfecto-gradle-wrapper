import os
import sys
import json
import getopt
from datetime import datetime

task = ""
cloud = ""
hostname = ""
configFile = "configFile.json"
itmsServerUrl = "test-executor"
authFilePath = "c:\\Users\\hristo\\securityTokens.json"
token = ""
testMethodNames = ""
testClassNames = ""
device = ""
debug = False
stacktrace = False
deviceNames = []
config = {}
originalConfig = {}
commandTemplate = "C:\\Gradle\\gradle-6.5\\bin\\gradle.bat %s -PcloudURL=\"%s\" -PsecurityToken=\"%s\"" 
commandArguments = ()

print ("Starting execution at %s" % datetime.now())
print ("Arguments: %s" % sys.argv)

# Mandatory arguments
args = sys.argv[1:]
if len(args) < 1:
  print ("No task name provided. Use android or perfecto-android-inst or ios or perfecto-xctest")
  sys.exit(2)
if len(args) < 2:
  print ("No cloud name provided.")
  sys.exit(2)
else:
  task = args[0].lower()
  if 'android' in task: 
    task = 'perfecto-android-inst'
  elif task == 'ios' or task == 'xcuitest' or task == 'xctest':
    task = 'perfecto-xctest'

  else:
    print ("No valid task provided: '%s'. Use 'android-inst' or 'xctest'" % task)
    sys.exit(2)

print ("Running task %s" % task)

cloud = args[1]
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
    opts, args = getopt.getopt(
      sys.argv[3:], 
      "ha:f:i:c:m:d:t:P:", 
      ["--authFilePath=", "configFileLocation", "itmsServerUrl=", "testClassNames=", "testMethodNames=", "device=", "securityToken=", "debug", "stacktrace"])
except getopt.GetoptError as er:
    print ('Wrong arguments provided. Exiting.')
    print (er)
    sys.exit(2)

for opt, arg in opts:
  if opt == '-h':
    print ("Help yourself!")
    sys.exit()
  elif opt in ("-f", "--configFileLocation"):
    commandTemplate += " -PconfigFileLocation=\"%s\""
    configFile = arg
    commandArguments += (arg,)
    print ("Overwriting config file name '%s'" % configFile)
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
  elif opt in ("-d", "--device"):
    print ("Overwriting device id: " % device)    
  elif opt in ("--debug"):
    debug = True
    commandTemplate += " --debug"
    print ("Overwriting debug: True")    
  elif opt in ("-s", "--stacktrace"):
    stacktrace = True
    print ("Overwriting stacktrace: True")
    commandTemplate += " --stacktrace"
  elif opt.startswith('-P'):
    print ("Adding generic argument %s" % arg)
    commandTemplate += " -P%s" % arg


itmsServerUrl = itmsServerUrl if itmsServerUrl.endswith(".perfectomobile.com") else itmsServerUrl + ".perfectomobile.com"
itmsServerUrl = "https://%s" % itmsServerUrl

print ("Running on cloud %s" % hostname)

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

if itmsServerUrl != "https://test-executor.perfectomobile.com":
  command += " -PitmsServerUrl=\"%s\"" % itmsServerUrl

print ("Executing command:\n%s\n" % command)

os.system(command)

# if len(deviceNames) > 0:
  # with open(configFile, "w") as w:
    # print ("Restoring original config file %s" % configFile)
    # json.dump(config, w, indent=4)
print ("Finished execution at %s" % datetime.now())