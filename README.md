tdlib-python
============

Python wrapper for Telegram tdlib

https://core.telegram.org/tdlib



Libraries `lib/libtdjson.so` , `lib/tdjson32.dll` and `lib/tdjson64.dll` were compiled from the original td repository:

https://github.com/tdlib/td


For quick test
==============

`python -i main.py`



To send message
---------------

```
td_send({'@type': 'sendMessage',
         'chat_id': chat_id,
         'input_message_content': {
             '@type': 'inputMessageText',
             'text': {
                 '@type': 'formattedText',
                 'text': 'test'
             }
         }})
```
