# tdlib-python

Python wrapper for Telegram tdlib

https://core.telegram.org/tdlib


Libraries `lib/libtdjson.so` , `lib/tdjson32.dll` and `lib/tdjson64.dll` were compiled from the original td repository: https://github.com/tdlib/td


## Example


```
git clone https://github.com/JunaidBabu/tdlib-python.git
cp local_settings_sample.py local_settings.py
# update local_settings.py
cd tdlib-python
python3 echo.py
```


## Other snippets

### To send message

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
