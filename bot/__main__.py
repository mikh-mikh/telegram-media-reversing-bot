import os
from re import search
from pyrogram import Client, filters
from bot import app, data, download_dir
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.helper.utils import add_task_video, add_task_ytvideo, add_task_audio, add_task_photo


# Define the handler functions for the tasks (task_text or task_audio or task_video or task_video_random)

# task_text reverses text messages or videos from external links (non-telegram)
def task_text(client, message):
    yt_url = 'www.youtube|youtu.be' # this is one variable for ytoutube links - we can add more vars for another links (fb, tiktok, etc)
    if search(yt_url, message.text):  # it checks for youtube links and run task_ytvideo. we can add more checkers for another external links (fb, tiktok, etc) 
        message.reply_text("you must to wait bro")
        add_task_ytvideo(message)
    else:      
        message.reply_text(message.text[::-1], quote=True) # this replies message with reversed text (fully - strings (from right to left) and position (from tail to head))
    pass

# photo_task working with photo by task_photo(it is reversing static photo by ffmpeg - because it is simpliest way for me)
def task_photo(client, message):
    message.reply_text("ЪУЬ", quote=True) # reply with funny message
    data.append(message)
    add_task_photo(message)
    pass
# task_video revesing telegram video or atached video from device. it called by handler with filter
def task_video(app, video_message):
      video_message.reply_text("Don't forget to show your friends", quote=True)
      data.append(video_message)
      add_task_video(video_message)
      pass
# 
def task_video_random(client, message):
    # Your code for video_random
    pass

# Add handlers for different types of messages (task_text or task_audio or task_video or task_video_random) and callback_query handler

# this text task may be executing here  - but i did it by "task_text"
@app.on_message(filters.text)
def text_handler(client, message):
    task_text(client, message)

# static photo handler
@app.on_message(filters.incoming & (filters.photo))
def text_handler(client, message):
    task_photo(client, message)    

# audio handler (music\voices - they are one thing for ffmpeg)
@app.on_message(filters.incoming & (filters.audio | filters.voice))
def reverse_audio(app, message):
      message.reply_text("Good music is that it sounds both forward and in reverse. \
      Did you know that there can be hidden messages backwards in music?", quote=True) # motivate message to try a variety of music (children usually threw off the phonk - which upset me, it’s disgusting in any case)
      data.append(message)
      add_task_audio(message)

# video handler with options (videos, video notes, gifs - the are one thing for ffmpeg)
@app.on_message(filters.incoming & (filters.video | filters.video_note | filters.animation ))
def video_handler(app, message):
    global video_message
    video_message = message
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("rever", callback_data = "1"), InlineKeyboardButton("rever_random", callback_data = "2")]]
    )
    message.reply_text("Choose an option:", reply_markup=markup)

# callback handler for messages from video handler (2 buttons with question) 
@app.on_callback_query()
def handle_callback_query(app, callback_query):
      if callback_query.data == "1":
        task_video(app, video_message)
      elif callback_query.data == "2":
        video_message.reply_text("When I implement this then the result can be frightening", quote=True)

# Run the bot
app.run()
