from ctypes.util import find_library
from ctypes import *
import json
import sys

#tdjson_path = find_library("libtdjson.so") or "tdjson.dll"
#if tdjson_path is None:
#    print('can\'t find tdjson library')
#    quit()
# tdjson = CDLL(tdjson_path)
tdjson = CDLL("absolute path to libtdjson.so")
td_json_client_create = tdjson.td_json_client_create
td_json_client_create.restype = c_void_p
td_json_client_create.argtypes = []

td_json_client_receive = tdjson.td_json_client_receive
td_json_client_receive.restype = c_char_p
td_json_client_receive.argtypes = [c_void_p, c_double]

td_json_client_send = tdjson.td_json_client_send
td_json_client_send.restype = None
td_json_client_send.argtypes = [c_void_p, c_char_p]

td_json_client_execute = tdjson.td_json_client_execute
td_json_client_execute.restype = c_char_p
td_json_client_execute.argtypes = [c_void_p, c_char_p]

td_json_client_destroy = tdjson.td_json_client_destroy
td_json_client_destroy.restype = None
td_json_client_destroy.argtypes = [c_void_p]

td_set_log_file_path = tdjson.td_set_log_file_path
td_set_log_file_path.restype = c_int
td_set_log_file_path.argtypes = [c_char_p]

td_set_log_max_file_size = tdjson.td_set_log_max_file_size
td_set_log_max_file_size.restype = None
td_set_log_max_file_size.argtypes = [c_longlong]

td_set_log_verbosity_level = tdjson.td_set_log_verbosity_level
td_set_log_verbosity_level.restype = None
td_set_log_verbosity_level.argtypes = [c_int]

fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
td_set_log_fatal_error_callback.restype = None
td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]

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

print(td_execute({'@type': 'getTextEntities', 'text': '@telegram /test_command https://telegram.org telegram.me', '@extra': ['5', 7.0]}))

td_receive()

td_send({'@type': 'getAuthorizationState', '@extra': 1.01234})


td_send({'@type': 'setTdlibParameters', 'parameters': {'use_test_dc': False, 'api_id':94575, 'api_hash': 'a3406de8d171bb422bb6ddf3bbd800e2', \
    'device_model': 'Desktop', 'system_version': 'Unknown', 'system_language_code': 'en'}})

td_send({'@type': 'checkDatabaseEncryptionKey', 'encryption_key': 'randomencryptionkeyhere'})

td_send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': '+xxxxxxxx', 'allow_flash_call': False, 'is_current_phone_number': False})



td_send({'@type': 'checkAuthenticationCode', 'code': 'xxxx'})

td_send({'@type': 'checkAuthenticationPassword', 'password': 'xxxxxxxx'})



from time import gmtime, strftime
users = {}


while True:
    event = td_receive()
    if event:
        #print(event)
        #print('')
        if event.get('@type') == "updateUserStatus":
            if users.get(event.get('user_id')):
                striz = strftime("%Y-%m-%d %H:%M:%S") +"| "+event.get('status').get('@type')+"| "+users.get(event.get('user_id')).get('first_name')
                print(striz)
            else:
                td_send({'@type': 'getUser', 'user_id': event.get('user_id')})
        elif event.get('@type') == "user":
            users[event.get('id')] = event

td_json_client_destroy(client)



