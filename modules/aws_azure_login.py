import subprocess


def azure_login():

    is_logged_in = False

    login = subprocess.Popen(['aws-azure-login', '--no-prompt'], shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    login.wait()

    # Verify login status
    login_verify = subprocess.Popen(['aws', 'sts', 'get-caller-identity'], shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = login_verify.communicate()
    login_verify.wait()
    # print(output)

    if 'UserId' in output:
        is_logged_in = True

    return is_logged_in
