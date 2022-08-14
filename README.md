# LeDindoBOT

Fork of LeixBOT created by Leix/Leochely.

## Installation

Create a .env file with the following variables and format:

```
ACCESS_TOKEN=bot_token
CLIENT_SECRET=channel_token
BOT_PREFIX=!
CHANNEL=your_twitch_channel[stream, not bot]
INITIAL_CHANNELS=your_twitch_channel[stream, not bot]
```

To generate the access token, go to the twitch [token generator](https://twitchtokengenerator.com/), login as your **bot account** and select "bot chat token".
To generate the channel access token, go to the [token generator](https://twitchtokengenerator.com/), login as your **own account** and choose "custom scope token". Select all the permissions and generate the token.

I recommend making a virtual environment using python 3.9.x or above:

Debian/Ubuntu : 
```
apt install -y python3 python3-pip
```

RedHat/CentOS/Rocky:
```
yum install -y python3 python3-pip
```

Alpine :
```
apk add python3 py3-pip
```

SUSE/openSUSE :
```
zypper install python3 python3-pip
```


Then :
```
python3 -m pip install pipenv
python3 -m pipenv --python 3.9
python3 -m pipenv install -r requirements.txt
```

To use custom commands and custom routines, you have to use a SGBD; Here I use MariaDB, but you can also use PostgreSQL or MySQL for example; so you will have to edit the script custom_commands.py in consequence.
The file TWITCH_BOT.sql is avaliable to build easily the database from the dump.


## Usage

```
python3 -m pipenv run python bot.py
```

A Procfile is included for heroku deployment.

Use ctrl-C to stop the bot.
