import subprocess

# needs to reference clients.txt to translate client_name into correct profile name

def azure_login(client_name):

    is_logged_in = False
    login = subprocess.Popen(['aws-azure-login', '--profile', client_name], shell=True)
    login.wait()

    # Verify login status
    login_verify = subprocess.Popen(['aws', 'sts', 'get-caller-identity', '--profile', client_name], shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = login_verify.communicate()
    login_verify.wait()
    # print(output)

    if 'UserId' in output:
        is_logged_in = True

    return is_logged_in, profile_name
