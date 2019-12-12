# THIS BOT HAS BEEN MERGED TO HEMPPA AND IS DISCONTINUED

Hemppa is a modular bot with lot of features and one of the
modules is location bot - use this instead: https://github.com/vranki/hemppa




# Malobot - Matrix location bot

Location messages are not supported by any known Matrix
clients yet. This bot will translate any sent locations to links to
OpenStreetMap service so that they can be viewed with any client.

## First

* Create a Matrix user
* Get user's access token - In Riot Web see Settings / Help & about

## Running on host

Run something like:

``` bash
pip3 install pipenv
pipenv shell
pipenv install
MATRIX_USER="@user:matrix.org" MATRIX_ACCESS_TOKEN="MDAxOGxvYlotofcharacters53CgYAYFgo" MATRIX_SERVER="https://matrix.org" JOIN_ON_INVITE=True python3 bot.py
```

## Running with Docker

Create .env file and set variables:

``` bash
MATRIX_USER=@user:matrix.org
MATRIX_ACCESS_TOKEN=MDAxOGxvYlotofcharacters53CgYAYFgo
MATRIX_SERVER=https://matrix.org
JOIN_ON_INVITE=True
```

Note: without quotes!

Just run:

``` bash
docker-compose up
```

## Env variables

User, access token and server should be self-explanatory. Set JOIN_ON_INVITE to anything if you want the bot to
join invites automatically.

You can set MATRIX_PASSWORD if you want to get access token. Normally you can use Riot to get it.

## Testing

Say !loc [location name] in a room where the bot is - it will send a location and reply to itself with map link.
