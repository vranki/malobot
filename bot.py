import asyncio
import os
import json
from nio import (AsyncClient, RoomMessageText, RoomMessageUnknown)

client = None

def get_room_id(room):
    global client
    for roomid in client.rooms:
        if client.rooms[roomid].named_room_name() == room.named_room_name():
            return roomid
    print('Cannot find id for room', room.named_room_name(), ' - is the bot on it?')
    return None

async def message_cb(room, event):
    global client

    if event.body == '!loc':
        locationmsg = {
            "body": "Tampere, Finland",
            "geo_uri": "geo:61.5,23.766667",
            "msgtype": "m.location",
        }
        await client.room_send(get_room_id(room), 'm.room.message', locationmsg)

async def unknown_cb(room, event):
    if event.msgtype != 'm.location':
        return

    location_text = event.content['body']

    # Fallback if body is empty
    if len(location_text) == 0:
        location_text = 'location'

    sender_response = await client.get_displayname(event.sender)
    sender = sender_response.displayname

    geo_uri = event.content['geo_uri']
    latlon = geo_uri.split(':')[1].split(',')

    # Sanity checks to avoid url manipulation
    float(latlon[0])
    float(latlon[1])

    osm_link = 'https://www.openstreetmap.org/?mlat=' + latlon[0] + "&mlon=" + latlon[1]

    location_link_msg = {
        "body": sender + ": " + location_text + ' - ' + osm_link,
        "format": "org.matrix.custom.html",
        "msgtype": "m.text"
    }
    await client.room_send(get_room_id(room), 'm.room.message', location_link_msg)


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
