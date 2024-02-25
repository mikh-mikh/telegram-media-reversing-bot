# Telegram media reverser Bot
A Telegram bot to reverse Telegram media (messages, video, audio, gif, flip satatic images, text) via ffmpeg and python - for fun and learning.

### Requirements:

python3 machine with internet access (like your computer behind NAT) to telegram and youtube servers

### Configuration
Add values in environment variables or add them in [config.env.template](./config.env.template) and rename file to `config.env`.
- `API_ID` - Get it by creating an app on [https://my.telegram.org](https://my.telegram.org)
- `API_HASH` - Get it by creating an app on [https://my.telegram.org](https://my.telegram.org)
- `BOT_TOKEN` - Get it by creating a bot on [https://t.me/BotFather](https://t.me/BotFather)
- `SUDO_USERS` - Chat identifier of the sudo user. For multiple users use space as seperator. (not used)
- `DOWNLOAD_DIR` - (Optional) Temporary download directory to keep downloaded files. I recommend to use ramfs (/dev/shm/ in linux) - to speedup transcoding.
- `SEGMENT_SIZE` - Setting the segmentation size. Big files are segmented (libx264 50MB input\segment needs for 16GB free RAM) for procesing.

### Configuring Encoding Format
Encoder settings are harcoded because i do not have any HW accels now.

To experiment and change encoder and encode settings try to edit them ($video_opts string vars) in [ffmpeg_utils.py](/bot/helper/ffmpeg_utils.py):

Windows + intel CPU (ivy bridge+):
```
-c:v h264_qsv
```
Windows\Linux + nvidia card (kepler+ with nvidia drivers) (it is not checked by me - it is by example - you need to experiment with $video_opts):
```
-c:v nvenc
```
For audio it is using lib3lame codec (mp3) (hardcoded now), To experiment and change encoder and encode settings try to edit them in [ffmpeg_utils.py](/bot/helper/ffmpeg_utils.py):
```
-с:a lib3lame
```
see and follow comments in code

### Configuring RAM usage
see `SEGMENT_SIZE` entry. There are no calculations, but you can set `SEGMENT_SIZE` in 50MB for 16GB RAM home PC (this is the setup for my laptop with 2 browser windows open) and increase if necessary

### Configuring messges and promts:
To change bot messages (greetings, replies) just find and edit them in [utils.py, __main.py__](bot/helper/utils.py, bot/__main.py__)  

### Installing Requirements

Bare:
Install ffmpeg and required Python Modules in your machine:

Linux (deb distro in example):

```sh
git clone 
apt-get install ffmpeg python3-pip
cd media-reverser-bot
pip3 install -r requirements.txt
```

Windows:
- install ffmpeg from official installer (ffmpeg.org) (ffmpeg calls from python - portable or compiled ffmpeg binaries must be in PATH)
- install python3 from official installer
- clone\copy repo to folder
- install pip modules from requirements.txt

```windows cmd
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

```windows cmd (in media-reverser-bot dir)
python -m bot
```

### Planned improvements:
- servless running (to deploy in servless cloud instances)
- set codec settings in config.env
- set any setting in config.env

### Credits

*Thanks to [ShannonScott](https://gist.github.com/ShannonScott) for [transcode_h265.py](https://gist.github.com/ShannonScott/6d807fc59bfa0356eee64fad66f9d9a8)*
*Thanks to [Adnan Ahmad](https://gist.github.com/viperadnan-git) for Video Encoder Bot*
*Thanks to friends for this idiotic idea, testing, and fun content generated by them*
*Thanks to chatgpt*

### Copyright & License
- Copyright &copy; 2022 &mdash; [Mikhail Sadchikov](https://github.com/mikh-mikh)
- Licensed under the terms of the [GNU General Public License Version 3 &dash; 29 June 2007](./LICENSE)
