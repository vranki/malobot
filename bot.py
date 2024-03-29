import asyncio
import os
import json
from nio import (AsyncClient, RoomMessageText, RoomMessageUnknown, JoinError, InviteEvent)
from geopy.geocoders import Nominatim

client = None

async def send_html(body, client, room):
    msg = {
        "body": body,
        "msgtype": "m.text"
    }
    await client.room_send(get_room_id(room), 'm.room.message', msg)

def get_room_id(room):
    global client
    for roomid in client.rooms:
        if client.rooms[roomid].named_room_name() == room.named_room_name():
            return roomid
    print('Cannot find id for room', room.named_room_name(), ' - is the bot on it?')
    return None

async def message_cb(room, event):
    global client

    if event.body.startswith('!loc'):
        locationmsg = {
            "body": "Tampere, Finland",
            "geo_uri": "geo:61.5,23.766667",
            "msgtype": "m.location",
        }
        if len(event.body) > 6:
            query = event.body[4:]
            geolocator = Nominatim(user_agent="Matrix_location_bot")
            location = geolocator.geocode(query)
            if location:
                locationmsg['body'] = location.address
                locationmsg['geo_uri'] = 'geo:' + str(location.latitude) + ',' + str(location.longitude)
            else:
                await send_html("Can't find " + query + " on map!", client, room)
                return

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
    
    body = sender + ' - ' + osm_link
    await send_html(body, client, room)

async def invite_cb(room, event):
    for attempt in range(3):
        result = await client.join(room.room_id)
        if type(result) == JoinError:
            print(f"Error joining room {room.room_id} (attempt %d): %s",
                attempt, result.message,
            )
        else:
            break

async def main():
    global client
    access_token = os.getenv('MATRIX_ACCESS_TOKEN')
    join_on_invite = os.getenv('JOIN_ON_INVITE')

    client = AsyncClient(os.environ['MATRIX_SERVER'], os.environ['MATRIX_USER'])
    if access_token:
        client.access_token = access_token
    else:
        await client.login(os.environ['MATRIX_PASSWORD'])
        print("Access token:", client.access_token)
    await client.sync()
    if client.logged_in:
        client.add_event_callback(message_cb, RoomMessageText)
        client.add_event_callback(unknown_cb, RoomMessageUnknown)
        if join_on_invite:
            print('Note: Bot will join rooms if invited')
            client.add_event_callback(invite_cb, (InviteEvent,))
        print('Bot running')
        await client.sync_forever(timeout=30000)
    else:
        print('Client was not able to log in, check env variables!')

asyncio.get_event_loop().run_until_complete(main())
