from local_settings import bot_token, api_id, api_hash, dir_path
from tdLib.client import Client

client = Client()


def auth_callback(data):
    print(data)
    update_type = data.get("@type")
    if update_type == "authorizationStateWaitTdlibParameters":
        client.sendCommand(
            {
                "@type": "setTdlibParameters",
                "parameters": {
                    "use_test_dc": False,
                    "api_id": api_id,
                    "api_hash": api_hash,
                    "device_model": "Desktop",
                    "system_version": "Unknown",
                    "application_version": "0.0",
                    "system_language_code": "en",
                    "database_directory": dir_path + "/tdLib/Database",
                    "files_directory": dir_path + "/tdLib/Files",
                    "use_file_database": True,
                    "use_chat_info_database": True,
                    "use_message_database": True,
                    "enable_storage_optimizer": False,
                    "ignore_file_names": True,
                },
            },
            auth_callback,
        )
    elif update_type == "authorizationStateWaitEncryptionKey":
        client.sendCommand(
            {
                "@type": "checkDatabaseEncryptionKey",
                "encryption_key": "randomencryption",
            },
            auth_callback,
        )
    elif update_type == "authorizationStateWaitPhoneNumber":
        client.sendCommand(
            {"@type": "checkAuthenticationBotToken", "token": bot_token}, auth_callback
        )
    elif update_type == "ok":
        client.sendCommand({"@type": "getAuthorizationState"}, auth_callback)
    elif update_type == "authorizationStateReady":
        pass  # things begin here


def updateNewMessageListener(event_msg):
    if event_msg["@type"] != "updateNewMessage":
        return
    if event_msg["message"]["is_outgoing"]:
        return
    chat_id = event_msg["message"]["chat_id"]
    client.sendCommand(
        {
            "@type": "sendMessage",
            "chat_id": chat_id,
            "input_message_content": {
                "@type": "inputMessageText",
                "text": {"@type": "formattedText", "text": "Echo"},
            },
        }
    )
    pass


client.addListener(updateNewMessageListener)
client.sendCommand({"@type": "getAuthorizationState"}, auth_callback)
client.idle()
