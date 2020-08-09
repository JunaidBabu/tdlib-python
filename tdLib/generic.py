from ctypes import CDLL, c_void_p, c_char_p, c_double, c_int, c_longlong, CFUNCTYPE
from ctypes.util import find_library
import os
import json
import logging
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))

if os.name == "posix":
    tdjson = CDLL(dir_path + "/libtdjson.so.1.6.4")
else:
    CDLL(dir_path + "/zlibd1.dll")
    tdjson = CDLL(dir_path + "/tdjson64.dll")

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

fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
td_set_log_fatal_error_callback.restype = None
td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]


def on_fatal_error_callback(error_message):
    print("TDLib fatal error: ", error_message)
    # logging.error('TDLib fatal error: ', error_message)


# td_set_log_verbosity_level(2)
c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
td_set_log_fatal_error_callback(c_on_fatal_error_callback)


def td_send(_client, query):
    query = json.dumps(query).encode("utf-8")
    td_json_client_send(_client, query)


def td_receive(_client):
    result = td_json_client_receive(_client, 2.0)
    if result:
        result = json.loads(result.decode("utf-8"))
    return result


def td_execute(_client, query):
    query = json.dumps(query).encode("utf-8")
    result = td_json_client_execute(_client, query)
    if result:
        result = json.loads(result.decode("utf-8"))
    return result
