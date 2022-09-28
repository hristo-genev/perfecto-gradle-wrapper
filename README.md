# perfecto-gradle-wrapper
A wrapper of the perfecto gradle plugin which allows automatic selection of security tokens based on the cloud name provided and simplified syntax.

# Usage
`./gradle-perfecto.py android-inst <cloud-name>
`./gradle-perfecto.py android <cloud-name>

`./gradle-perfecto.py xctest <cloud-name>
`./gradle-perfecto.py ios <cloud-name>

`./gradle-perfecto.py ios <cloud-name> -f <path-to-json-config-file> 

`./gradle-perfecto.py --help for more

The cloud tokens are saved in JSON format in a token storage file.
{
  "tokens": {
    "<cloud-name>": "<YOUR_TOKEN_HERE>"
    }
}
