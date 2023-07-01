import modules.login_config as lcfg
import aws_sso_lib
import subprocess


def aws_login(login_type, profile, client_name, logger, start_url=None, sso_region=None):
    is_logged_in = False

    if login_type == 'aal':
        profile_name = profile['profile_name']

        # Set certain aws-azure-login environmental variables - still needed
        lcfg.set_login_credentials(profile, profile_name)

        logger.info(f'\nLogging in to {profile_name}. Enter your Azure credentials in '
                    f'the popup window.')

        # Run 'aws-azure-login --profile foo --mode gui' in a subprocess shell
        login = subprocess.Popen(['aws-azure-login', '--profile', f'{profile_name}', '--mode', 'gui'],
                                 shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = login.communicate()
        logger.debug(output)
        logger.debug(errors)
        login.wait()

        # Verify login status with an STS API call
        login_verify = subprocess.Popen(['aws', 'sts', 'get-caller-identity'], shell=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = login_verify.communicate()
        logger.debug(output)
        logger.debug(errors)
        login_verify.wait()

        if 'UserId' in output:
            logger.info(f'You are logged in to {profile_name}.')
            is_logged_in = True

    else:
        # start_url = profile['start_url']
        # sso_region = profile['sso_region']

        logger.info(f'\nLogging in to {client_name}. Enter your credentials in the browser window.')

        login_response = aws_sso_lib.login(start_url, sso_region)

        if login_response['accessToken']:
            logger.info(f'You are logged in to {client_name}.')
            is_logged_in = True

    return is_logged_in
