import os, time, re
from pytube import YouTube
from pathlib import Path
from bot import data, download_dir
from pyrogram.types import Message
from .ffmpeg_utils import encode_audio, encode_video, encode_photo, get_thumbnail, get_duration, get_width_height

def on_task_complete():
    del data[0]
    #if len(data) > 0:
      #add_task(data[0])

def add_task_photo(message: Message):
    try:
      msg = message.reply_text("dwlding...", quote=True)
      filepath = message.download(file_name=download_dir)
      msg.edit("reversing...")
      new_file = encode_photo(filepath)
      if new_file:
           width, height = get_width_height(new_file)
           message.reply_photo(new_file)
           os.remove(thumb)
           msg.edit("reversed")
      else:
           msg.edit("Something wents wrong while encoding your file")
           os.remove(filepath)
    except Exception as e:
        
       msg.edit(f"{e}")
    on_task_complete()

def add_task_video(message: Message):
    try:
      msg = message.reply_text("dwlding...", quote=True)
      filepath = message.download(file_name=download_dir)
      msg.edit("reversing...")
      new_file = encode_video(filepath)
      if new_file:
           msg.edit("Reversed, I'm making a tumbnail...")
           duration = get_duration(new_file)
           thumb = get_thumbnail(new_file, download_dir, duration / 4)
           width, height = get_width_height(new_file)
           msg.edit("uploading...")
           message.reply_video(new_file, quote=True, supports_streaming=True, thumb=thumb, duration=duration, width=width, height=height)
           os.remove(new_file)
           os.remove(thumb)
           msg.edit("reversed")
      else:
           msg.edit("Something wents wrong while encoding your file.")
           os.remove(filepath)
    except Exception as e:

        msg.edit(f"{e}")
        
    on_task_complete()

def add_task_audio(message: Message):
    try:
      msg = message.reply_text("dwlding...", quote=True)
      filepath = message.download(file_name=download_dir)
      msg.edit("reversing...")
      new_file = encode_audio(filepath)
      if new_file:
           msg.edit("Reversed, I'm making a tumbnail...")
           duration = get_duration(new_file)
           thumb = get_thumbnail(new_file, download_dir, duration / 4)
           width, height = get_width_height(new_file)
           msg.edit("uploading...")
           message.reply_video(new_file, quote=True, supports_streaming=True, thumb=thumb, duration=duration, width=width, height=height)
           os.remove(new_file)
           os.remove(thumb)
           msg.edit("reversed")
      else:
           msg.edit("Something wents wrong while encoding your file. Make sure it is not already in HEVC format.")
           os.remove(filepath)
    except Exception as e:

       msg.edit(f"{e}")
        
    on_task_complete()

def add_task_ytvideo(message: Message):
    try:
      msg = message.reply_text("dwlding...", quote=True)
      yt = YouTube(message.text)  # we get youtube link as a str from message
      filepath = yt.streams.filter(progressive=True, file_extension='mp4', res='360p').order_by('resolution').desc().first().download(download_dir) # 360p may be not presenting on youtube.
      new_file = encode_video(filepath)
      if new_file:
           msg.edit("Reversed, I'm making a tumbnail...")
           duration = get_duration(new_file)
           thumb = get_thumbnail(new_file, download_dir, duration / 4)
           width, height = get_width_height(new_file)
           msg.edit("uploading...")
           message.reply_video(new_file, quote=True, supports_streaming=True, thumb=thumb, duration=duration, width=width, height=height)
           os.remove(new_file)
           os.remove(thumb)
           msg.edit("reversed")
      else:
           msg.edit("Something wents wrong while encoding your file. Make sure it is not already in HEVC format.")
           os.remove(filepath)
    except Exception as e:

        msg.edit(f"{e}")