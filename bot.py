import asyncio
import os
from nio import (AsyncClient, RoomMessageText)

async def message_cb(room, event):
    print(
        "Message received for room {} | {}: {}".format(
            room.display_name, room.user_name(event.sender), event.body
        )
    )

async def main():
    access_token = os.getenv('MATRIX_ACCESS_TOKEN')
    client = AsyncClient(os.environ['MATRIX_SERVER'], os.environ['MATRIX_USER'])
    if access_token:
        client.access_token = access_token
    else:
        await client.login(os.environ['MATRIX_PASSWORD'])
    print("at:", client.access_token)
    await client.sync()
    print('End init sync')
    client.add_event_callback(message_cb, RoomMessageText)
    await client.sync_forever(timeout=30000)

asyncio.get_event_loop().run_until_complete(main())
