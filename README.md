# Telegram media reverser Bot
A Telegram bot to reverse Telegram media (messages, video, audio, gif, flip satatic images, text) via ffmpeg and python - for fun.

### Requirements:
A lot, LOT of RAM
you need to have over 16GB RAM for reversing ~15 minutes content in ~480p quiality
python3 machine with internet access to telegram and yputube servers (it works under NAT)

### Configuration
Add values in environment variables or add them in [config.env.template](./config.env.template) and rename file to `config.env`.
- `API_ID` - Get it by creating an app on [https://my.telegram.org](https://my.telegram.org)
- `API_HASH` - Get it by creating an app on [https://my.telegram.org](https://my.telegram.org)
- `BOT_TOKEN` - Get it by creating a bot on [https://t.me/BotFather](https://t.me/BotFather)
- `SUDO_USERS` - Chat identifier of the sudo user. For multiple users use space as seperator. (not used)
- `DOWNLOAD_DIR` - (Optional) Temporary download directory to keep downloaded files.

### Configuring Encoding Format
To change the ffmpeg profile edit them in [ffmpeg_utils.py](/bot/helper/ffmpeg_utils.py):

Windows + intel CPU (ivy bridge+):
```
-c:v h264_qsv
```
Windows\Linux + nvidia card (kepler+):
```
-c:v nvenc
```

### Configuring messges and promts:
To change bot messages (greetings, replies) just edit these in [utils.py, __main.py__](bot/helper/utils.py, bot/__main.py__)  

### Installing Requirements

Bare:
Install ffmpeg and required Python Modules in your machine:

Linux (deb in example):

```sh
git clone 
apt-get install ffmpeg python3-pip
cd media-reverser-bot
pip3 install -r requirements.txt
```

Windows:
- install ffmpeg from official installer (ffmpeg.org)
- install python3
- copy repo to folder

```cmd
cd media-reverser-bot
pip install -r requirements.txt
```

### Deployment
With python3.7 or later.

```sh (in media-reverser-bot dir)
python3 -m bot
or 
nohup python3 -m bot &
```
windows cmd (in media-reverser-bot dir)
```
python -m bot
```
### Planned improvements:
- servless running (to deploy in servless cloud instance) (it is fun but my computer will )
- work with big files

### Credits
*Thanks to [ShannonScott](https://gist.github.com/ShannonScott) for [transcode_h265.py](https://gist.github.com/ShannonScott/6d807fc59bfa0356eee64fad66f9d9a8)*
*Thanks to [Adnan Ahmad](https://gist.github.com/viperadnan-git) for Video Encoder Bot
*Thanks to friends for this idiotic idea, testing, and fun content generated by them
### Copyright & License
- Copyright &copy; 2022 &mdash; [Mikhail Sadchikov](https://github.com/mikh-mikh)
- Copyright &copy; 2021 &mdash; [Adnan Ahmad](https://github.com/viperadnan-git)
- Licensed under the terms of the [GNU General Public License Version 3 &dash; 29 June 2007](./LICENSE)