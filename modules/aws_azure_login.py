import subprocess
from src import clients


def azure_login(profile_names):

    is_logged_in = False
    for name in profile_names:
        # Log in to an account using its profile name
        login = subprocess.Popen(['aws-azure-login', '--profile', name], shell=True)
        login.wait()

        # Verify login status
        login_verify = subprocess.Popen(['aws', 'sts', 'get-caller-identity', '--profile', name], shell=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = login_verify.communicate()
        login_verify.wait()
        # print(output)

        if 'UserId' in output:
            is_logged_in = True

    return is_logged_in
