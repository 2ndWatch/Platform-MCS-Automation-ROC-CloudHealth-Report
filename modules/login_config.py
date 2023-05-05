import subprocess


def are_profiles_configured():
    profiles = subprocess.Popen(['aws', 'configure', 'list-profiles'], shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = profiles.communicate()
    profiles.wait()

    return 'ckempa' in output


def configure_login_credentials():
    print('\nYou configured the things!\n')
    return


result = are_profiles_configured()
print(result)
