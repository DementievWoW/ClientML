import json
import threading
import time

import websockets
import asyncio
import uuid

from MachineState import MachineState
from fileHandler import readStartLogs, readRuntimeLogs

# from fileHandler import readRuntimeLogs, readStartLogs

password = 'qwer'
UUID = str(uuid.UUID(int=uuid.getnode()))
# url = "ws://127.0.0.1:8000"
# url = "ws://localhost:8000/ws/"
url = "ws://localhost:8000/ws/?password=" + password + "&UUID=" + UUID

pathStartLogs ="src/launchlog.log"
pathRuntimeLogs="src/runtimelog.log"
def getMachineStateJson():
    data = {
        "UUID": str(uuid.UUID(int=uuid.getnode())),
        "machineState": [],
        "password": "qwer",
        "StartLogs": [],
        "RuntimeLogs": [],
    }
    data['StartLogs'].append(readStartLogs(pathStartLogs))
    data['RuntimeLogs'].append(readRuntimeLogs(pathRuntimeLogs))
    data['machineState'].append(MachineState().__dict__)
    print(UUID)
    data_json = json.dumps(data, ensure_ascii=False)
    return data_json

# async def connection(url):
#     async with websockets.connect(url) as websocket:
#         return websocket
# websocket = asyncio.get_event_loop().run_until_complete(connection(url))
async def listen(url):
    async with websockets.connect(url) as websocket:
        while 1:
            msg = await websocket.recv()
            print(msg)
            # time.sleep(10)
            await websocket.send(getMachineStateJson())
            # while 1:
            #     # time.sleep(10)
            #     await websocket.send(getMachineStateJson())


# async def listen(websocket):
#     while 1:
#         msg = await websocket.recv()
#         print(msg)

# async def sendData(websocket):
#     await websocket.send("fdsgfsgsfgfdsf")
#
#
# websocket = websockets.connect(url)
# listen(websocket)
# sendData(websocket)


# while 1:

# asyncio.get_event_loop().run_until_complete(listen(url))
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(listen(url))
# asyncio.get_event_loop().run_until_complete(listen(websocket))
# asyncio.get_event_loop().run_until_complete(sendData(websocket))
