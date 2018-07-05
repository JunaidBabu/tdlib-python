import getpass

from generic import *


def logout():
    td_send({'@type': 'logOut'})



print("Starting login sequence")

while True:
    event = td_receive()
    if event:
        print(event)
        if event.get('@type') == 'updateAuthorizationState':
            authtype = event.get('authorization_state').get('@type')
            if authtype == "authorizationStateWaitTdlibParameters":
                td_send({'@type': 'setTdlibParameters',
                     'parameters': {'use_test_dc': False,
                                    'api_id':94575,
                                    'api_hash': 'a3406de8d171bb422bb6ddf3bbd800e2',
                                    'device_model': 'Desktop',
                                    'system_version': 'Unknown',
                                    'application_version': "0.0",
                                    'system_language_code': 'en',
                                    'database_directory': 'Database',
                                    'files_directory': 'Files',
                                    'use_file_database': True,
                                    'use_chat_info_database': True,
                                    'use_message_database': True,
                                    }
                     })
            elif authtype == 'authorizationStateWaitEncryptionKey':
                td_send({'@type': 'checkDatabaseEncryptionKey', 'encryption_key': 'randomencryption'})
            elif authtype == "authorizationStateWaitPhoneNumber":
                phone = input('Enter phone number:')
                td_send({'@type': 'setAuthenticationPhoneNumber',
                         'phone_number': phone,
                         'allow_flash_call': False,
                         'is_current_phone_number': False}
                        )
            elif authtype == "authorizationStateWaitCode":
                code = input('Enter code:')
                td_send({'@type': 'checkAuthenticationCode', 'code': str(code)})
            elif authtype == "authorizationStateWaitPassword":
                password = getpass.getpass('Password:')
                td_send({'@type': 'checkAuthenticationPassword', 'password': password})
            elif authtype == "authorizationStateReady":
                break

# more awesome stuff here

# td_json_client_destroy(client)
