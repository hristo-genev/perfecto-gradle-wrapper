# perfecto-gradle-wrapper
A wrapper of the perfecto gradle plugin which allos automatic selection of security tokens based on the cloud name provided.

# Usage
./gradle-perfecto.py android-inst mobilcloud

./gradle-perfecto.py xctest mobilcloud


The cloud tokens are saved in JSON format in a token storage file.
{
  "tokens": {
    "mobilecloud": ""
    }
}
