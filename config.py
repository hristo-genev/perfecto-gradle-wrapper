import os
auth_file_path = os.getenv('PERFECTO_TOKEN_STORAGE')
if not auth_file_path:
    auth_file_path = os.path.join(os.path.expanduser("~"), "tokens.json")