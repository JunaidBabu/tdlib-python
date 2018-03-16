import json
import getpass

from generic import *

def on_fatal_error_callback(error_message):
    print('TDLib fatal error: ', error_message)

td_set_log_verbosity_level(2)
c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
td_set_log_fatal_error_callback(c_on_fatal_error_callback)

client = td_json_client_create()

def td_send(query):
    query = json.dumps(query).encode('utf-8')
    td_json_client_send(client, query)

def td_receive():
    result = td_json_client_receive(client, 1.0)
    if result:
        result = json.loads(result.decode('utf-8'))
    return result

def td_execute(query):
    query = json.dumps(query).encode('utf-8')
    result = td_json_client_execute(client, query)
    if result:
        result = json.loads(result.decode('utf-8'))
    return result


td_send({'@type': 'setTdlibParameters',
         'parameters': {'use_test_dc': False,
                        'api_id':94575,
                        'api_hash': 'a3406de8d171bb422bb6ddf3bbd800e2',
                        'device_model': 'Desktop',
                        'system_version': 'Unknown',
                        'system_language_code': 'en',
                        'database_directory': 'Database',
                        'files_directory': 'Data'
                        }
         })

td_send({'@type': 'checkDatabaseEncryptionKey', 'encryption_key': 'randomencryption'})

td_send({'@type': 'getAuthorizationState', '@extra': 1.01234})


# Login sequence
while True:
    event = td_receive()
    if event:
        print(event)
        if event.get('@type') == 'updateAuthorizationState':
            authtype = event.get('authorization_state').get('@type')
            if authtype == "authorizationStateWaitPhoneNumber":
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

td_json_client_destroy(client)

