from tdLib.generic import (
    td_receive,
    td_send,
    td_json_client_destroy,
    td_json_client_create,
    td_execute,
)
import asyncio


class Client:
    current_req = 0
    methods = []
    listeners = []
    loop = asyncio.get_event_loop()
    _client = td_json_client_create()

    async def __smallThread(self):
        while True:
            await asyncio.sleep(0)
            event = td_receive(self._client)
            if event:
                if "@extra" in event:
                    for m in self.methods:
                        if event["@extra"] == m[1]:
                            m[0](event)
                            self.methods.remove(m)
                for listener in self.listeners:
                    listener(event)

    def __init__(self):
        print(
            td_execute(
                self._client,
                {
                    "@type": "setLogVerbosityLevel",
                    "new_verbosity_level": 1,
                    "@extra": 1.01234,
                },
            )
        )
        self.loop.create_task(self.__smallThread())

    def idle(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.close()
            td_json_client_destroy(self._client)

    def addListener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    async def __sendCommand(self, command, callback=None):
        if callback:
            command["@extra"] = self.current_req
            self.methods.append((callback, self.current_req))
        td_send(self._client, command)
        print(command)
        self.current_req += 1

    def sendCommand(self, command, callback=None):
        self.loop.create_task(self.__sendCommand(command, callback))
        # self.__sendCommand(command, callback)
        print(command)
