import os
home_folder = os.getenv('USERPROFILE')
auth_file_path = os.path.join(home_folder, "securityTokens.json")
