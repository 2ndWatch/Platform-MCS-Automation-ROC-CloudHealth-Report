import subprocess
# import json
#
# with open('src/clients.txt') as cl:
#     cl_txt = cl.read()
#
# clients = json.loads(cl_txt)


def azure_login(client_keys, profile_name):

    is_logged_in = False
    login = subprocess.Popen(['aws-azure-login', '--profile', profile_name], shell=True)
    login.wait()

    # Verify login status
    login_verify = subprocess.Popen(['aws', 'sts', 'get-caller-identity', '--profile', profile_name], shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = login_verify.communicate()
    login_verify.wait()
    # print(output)

    if 'UserId' in output:
        is_logged_in = True

    return is_logged_in, profile_name
