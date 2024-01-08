# perfecto-gradle-wrapper
A wrapper of the perfecto gradle plugin which allows:
* simplified syntax
* automatic log parsing and coloring
* automatic job number incrementation
* automatic selection of security tokens based on the cloud name provided
* automatic report opening at the end of the run

# Usage
```
./perfecto-espresso.py -c <cloud-name>
./perfecto-xctext.py -c <cloud-name>

./perfecto-espresso.py -c <cloud-name> -f <path-to-json-config-file> --debug
./perfecto-xctext.py --help for more
```

The cloud tokens should be saved in a simple INI format in a token storage file pointed by the environment variable PERFECTO_TOKEN_STORAGE.
```
[tokens]
<cloud-name>: <YOUR_TOKEN_HERE>
<cloud-name-2>: <YOUR_TOKEN_HERE>
```
