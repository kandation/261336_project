import websocket
import random
import json
import time, datetime

print(random.randint(0,1023))
location_fake = ['Science Faculty', 'Engineering Faculty', 'CPE', 'Clock circus']

websocket.enableTrace(True)
#ws = websocket.create_connection("ws://188.166.212.91:9999/ww")
#ws = websocket.create_connection("ws://128.199.90.20:9999/ww")
ws = websocket.create_connection("ws://127.0.0.1:9999/ww")

while True:

    temp = {}
    for k in location_fake:
        ran = random.randint(0, 1023)
        temp['location'] = k
        temp['air'] = ran
        temp['timestamp'] = int(datetime.datetime.utcnow().timestamp())
        data = str(json.dumps(temp))
        print(data)
        ws.send(data)
        time.sleep(0.5)