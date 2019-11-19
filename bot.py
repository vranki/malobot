import asyncio
import os
import json
from nio import (AsyncClient, RoomMessageText, RoomMessageUnknown)

client = None

def get_room_id(room):
    global client
    for roomid in client.rooms:
        print(roomid, client.rooms[roomid].named_room_name())
        if client.rooms[roomid].named_room_name() == room.named_room_name():
            return roomid
    print('Cannot find id for room', room.named_room_name(), ' - is the bot on it?')
    return None

async def message_cb(room, event):
    global client
    print(
        "Message received for room {} | {}: {}".format(
            room.display_name, room.user_name(event.sender), event.body
        )
    )
    if event.body == '!loc':
        locationmsg = {
            "body": "Tampere, Finland",
            "geo_uri": "geo:61.5,23.766667",
            "msgtype": "m.location",
        }
        print('Sending location to room id', get_room_id(room))
        await client.room_send(get_room_id(room), 'm.room.message', locationmsg)

async def unknown_cb(room, event):
    if event.msgtype != 'm.location':
        return
    print('Yay! Got location:', event.content['geo_uri'], event.content['body'])

async def main():
    global client
    access_token = os.getenv('MATRIX_ACCESS_TOKEN')
    client = AsyncClient(os.environ['MATRIX_SERVER'], os.environ['MATRIX_USER'])
    if access_token:
        client.access_token = access_token
    else:
        await client.login(os.environ['MATRIX_PASSWORD'])
        print("Access token:", client.access_token)
    await client.sync()

    client.add_event_callback(message_cb, RoomMessageText)
    client.add_event_callback(unknown_cb, RoomMessageUnknown)
    print('Bot running')
    await client.sync_forever(timeout=30000)

asyncio.get_event_loop().run_until_complete(main())
