clients = {
    'a': {
        'name': 'CKE',
        'profiles': [
            {
                'account_name': 'CKE Restaurants MPA/Prod',
                'profile_name': 'ckempa',
                'account_number': '512176277481',
                'region': ['us-east-1', 'us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': '7b0eca21-b784-4d1c-9ca3-ce1300049e17'
            }
        ]
    },
    'b': {
        'name': 'Cypherworx',
        'profiles': [
            {
                'account_name': 'CypherWorx Main Account',
                'profile_name': 'cypherworxmain',
                'account_number': '372356060901',
                'region': ['us-east-1'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': '26ffb536-3d6c-4005-89a8-cdb4bf43940e'
            }
        ]
    },
    'c': {
        'name': 'Edmund Optics',
        'profiles': [
            {
                'account_name': 'Edmund Optics Main account',
                'profile_name': 'eomain',
                'account_number': '269180092429',
                'region': ['us-east-1', 'us-east-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': 'd054ef79-3919-490e-9eb2-ff2174149e7d'
            }
        ]
    },
    'd': {
        'name': 'Utilities International',
        # accounts are a hot mess right now: some are on account list but not in My Apps, some are in My Apps but
        # not on account list, some being polled by Cloud Health are ???
        'profiles': [
            {
                'account_name': 'internal',
                'profile_name': 'uiwombat',
                'account_number': '010949642540',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': '75572fc2-2e74-4169-a543-73ad6aac0cae'
            },
            {
                'account_name': 'financial',
                'profile_name': 'uifinancial',
                'account_number': '124778240328',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': '51a9fd48-6595-4799-b0c4-b6ffd229acb3'
            },
            # on account list but not in My Apps
            # {
            #     'account_name': 'customer-Wapa-dr',
            #     'profile_name': 'uiwapadr',
            #     'account_number': '260667475419',
            #     'region': ['us-east-2', 'us-west-2'],
            #     'tenant_id': '',
            #     'app_id_uri': ''
            # },
            # on account list but not in My Apps
            # {
            #     'account_name': 'customer-ElPaso-dr',
            #     'profile_name': 'uielpasodr',
            #     'account_number': '300175269874',
            #     'region': ['us-east-2', 'us-west-2'],
            #     'tenant_id': '',
            #     'app_id_uri': ''
            # },
            {
                'account_name': 'Wapa',
                'profile_name': 'uiwapa',
                'account_number': '409793285578',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': 'ab1b1b5c-9758-4444-87be-cbdf00485c73'
            },
            # on account list but not in My Apps
            # {
            #     'account_name': 'customer-Evergy',
            #     'profile_name': 'uievergy',
            #     'account_number': '410946731030',
            #     'region': ['us-east-2', 'us-west-2'],
            #     'tenant_id': '',
            #     'app_id_uri': ''
            # },
            # on account list but not in My Apps
            # {
            #     'account_name': 'customer-Evergy-dr',
            #     'profile_name': 'uievergydr',
            #     'account_number': '530801975448',
            #     'region': ['us-east-2', 'us-west-2'],
            #     'tenant_id': '',
            #     'app_id_uri': ''
            # },
            {
                'account_name': 'customer-ElPaso',
                'profile_name': 'uielpaso',
                'account_number': '591720369555',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': 'd81a94b1-3be9-478d-a196-2902e161e604'
            },
            {
                'account_name': 'librarian',
                'profile_name': 'uilibrarian',
                'account_number': '596683006098',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': '6c269b98-74c1-4490-8724-bfb06d4ab8b9'
            },
            # on account list but not in My Apps
            # {
            #     'account_name': 'wombat-dr',
            #     'profile_name': 'uiwombatdr',
            #     'account_number': '635732022292',
            #     'region': ['us-east-2', 'us-west-2'],
            #     'tenant_id': '',
            #     'app_id_uri': ''
            # },
            {
                'account_name': 'customers',
                'profile_name': 'uicustomers',
                'account_number': '640494380191',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': 'b3c35cad-347b-40c5-962d-8591cf1d5f7b'
            },
            {
                'account_name': 'customer-AustinEnergy',
                'profile_name': 'uiaustin',
                'account_number': '670035103958',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': 'd055151a-8978-4fbb-b6ca-9abd3a77472b'
            },
            {
                'account_name': 'shared-services',
                'profile_name': 'uishared',
                'account_number': '722963886105',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': '70db8f1d-1e7b-4cb4-8f2f-f217de7f2b51'
            },
            # on account list but not in My Apps
            # {
            #     'account_name': 'customer-AustinEnergy-dr',
            #     'profile_name': 'uiaustindr',
            #     'account_number': '890726708363',
            #     'region': ['us-east-2', 'us-west-2'],
            #     'tenant_id': '',
            #     'app_id_uri': ''
            # },
            {
                'account_name': 'customer-bhe',
                'profile_name': 'uibhe',
                'account_number': '378850973661',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': 'b40ef666-4332-4ae5-8526-634211dd753a'
            },
            {
                'account_name': 'customer-CenterPointEnergy',
                'profile_name': 'uicenterpoint',
                'account_number': '631174679383',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': 'debcf93b-4788-4a5c-a2f2-37f618752ea7'
            },
            {
                'account_name': 'customer-ConsumersEnergy',
                'profile_name': 'uiconsumers',
                'account_number': '003837565195',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': 'b079ddf2-6e3f-490e-9f68-4ab1bae74f22'
            },
            {
                'account_name': 'customer-otp',
                'profile_name': 'uiotp',
                'account_number': '161742078190',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': '2bf34299-2094-4de2-99da-c395b892d603'
            },
            {
                'account_name': 'customer-pge',
                'profile_name': 'uipge',
                'account_number': '227853323018',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': 'e48e648f-72f0-4742-b999-3893c6388ace'
            },
            {
                'account_name': 'customer-pseg',
                'profile_name': 'uipseg',
                'account_number': '467189845498',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': '4070eb9c-a2c4-4b86-93bb-4082d6a0d367'
            },
            {
                'account_name': 'UII_Test_Account',
                'profile_name': 'uitest',
                'account_number': '288453765162',
                'region': ['us-east-2', 'us-west-2'],
                'tenant_id': '8242a0a9-c415-4206-be39-06637ad2817a',
                'app_id_uri': 'aab084b0-9c8d-4369-8d95-a3af31bfab81'
            }
        ]
    },
    'e': {
        'name': 'VNS Health',
        # 9 accounts
        'profiles': [
            {
                'account_name': 'Dev',
                'profile_name': 'vnsdev',
                'account_number': '394721647414',
                'region': ['us-east-1'],
                'tenant_id': '',
                'app_id_uri': ''
            },
            {
                'account_name': 'MSO',
                'profile_name': 'vnsmso',
                'account_number': '765697202555',
                'region': ['us-east-1'],
                'tenant_id': '',
                'app_id_uri': ''
            },
            {
                'account_name': 'MSO-Test',
                'profile_name': 'vnsmsotest',
                'account_number': '034571914901',
                'region': ['us-east-1'],
                'tenant_id': '',
                'app_id_uri': ''
            },
            {
                'account_name': 'Production',
                'profile_name': 'vnsprod',
                'account_number': '387721966484',
                'region': ['us-east-1'],
                'tenant_id': '',
                'app_id_uri': ''
            },
            {
                'account_name': 'Regulated',
                'profile_name': 'vnsreg',
                'account_number': '059317571093',
                'region': ['us-east-1'],
                'tenant_id': '',
                'app_id_uri': ''
            },
            {
                'account_name': 'Sandbox',
                'profile_name': 'vnssand',
                'account_number': '173082462933',
                'region': ['us-east-1'],
                'tenant_id': '',
                'app_id_uri': ''
            },
            {
                'account_name': 'Shared Services',
                'profile_name': 'vnsshared',
                'account_number': '330383299209',
                'region': ['us-east-1'],
                'tenant_id': '',
                'app_id_uri': ''
            },
            {
                'account_name': 'Test',
                'profile_name': 'vnstest',
                'account_number': '498214724335',
                'region': ['us-east-1'],
                'tenant_id': '',
                'app_id_uri': ''
            },
            {
                'account_name': 'Transit',
                'profile_name': 'vnstransit',
                'account_number': '643066205191',
                'region': ['us-east-1'],
                'tenant_id': '',
                'app_id_uri': ''
            }
        ]
    },
    'done': 'multiple clients',
    None: 'None'
}
