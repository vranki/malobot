# Malobot - Matrix location bot

Location messages are not supported by any known Matrix
clients yet. This bot will translate any sent locations to links to
OpenStreetMap service so that they can be viewed with any client.

## First

 * Create a Matrix user
 * Get user's access token - In Riot Web see Settings / Help & about

## Running on host

Run something like:

```
pip3 install pipenv
pipenv shell
pipenv install
MATRIX_USER="@user:matrix.org" MATRIX_ACCESS_TOKEN="MDAxOGxvYlotofcharacters53CgYAYFgo" MATRIX_SERVER="https://matrix.org" python3 bot.py
```

## Running with Docker

Create .env file and set variables:

```
MATRIX_USER=@user:matrix.org
MATRIX_ACCESS_TOKEN=MDAxOGxvYlotofcharacters53CgYAYFgo
MATRIX_SERVER=https://matrix.org
```

Note: without quotes!


Just run:

```
docker-compose up
```

## Testing

Say !loc in a room where the bot is - it will send a location and reply to itself with map link.

