import os
import sys
import json
import time
import ffmpeg
from subprocess import call, check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

def get_codec(filepath, channel='v:0'):
    output = check_output(['ffprobe', '-v', 'error', '-select_streams', channel,
                            '-show_entries', 'stream=codec_name,codec_tag_string', '-show_entries', 'format=duration', '-of', 
                            'default=nokey=1:noprint_wrappers=1', filepath])
    return output.decode('utf-8').split()

def encode_photo(filepath):
    basefilepath, extension = os.path.splitext(filepath)
    output_filepath = basefilepath + 'lol' + '.jpg'
    assert(output_filepath != filepath)
    print(filepath)
    call(['ffmpeg', '-i', filepath,] + ['-vf'] + ['hflip'] + [output_filepath]) 
    os.remove(filepath)
    return output_filepath    

def encode_video(filepath):
    basefilepath, extension = os.path.splitext(filepath)
    if len(extension) > 0:
       output_filepath = basefilepath + 'lol' + extension # + '.HEVC' + '.mp4'
    else:
       output_filepath = basefilepath + 'lol' + '.mp4' # + '.HEVC' + '.mp4' 
       
    assert(output_filepath != filepath)
    print(filepath)
    video_codec = get_codec(filepath, channel='v:0')
    if video_codec == [] :  # music file with
       video_opts = '' 
    elif video_codec[0] == 'mjpeg': # it needs for some telegram audio files with covers - they may be saved as video - for ffmpeg static cover image is a video stream
       video_opts = '-c:v copy'

    else:
        
       video_opts = '-c:v libx264  -vf reverse' # -c:v it is a encode codec. in other platfoms (arm, nvidia, any HW accels) you can and should to experiment foe improving perfomance
     
    call(['ffmpeg', '-i', filepath,] + ['-af'] + ['areverse'] + video_opts.split() + [output_filepath]) # add , '-af areverse -vf reverse'
    os.remove(filepath)
    return output_filepath

def encode_audio(filepath):
    basefilepath, extension = os.path.splitext(filepath)
    output_filepath = basefilepath + 'lol' + '.mp3' # all audio trancsode to mp3. it is fast, you can try any codecs \
                                                    # you need to change extension ".mp3" here to any, and audiocodec in complex (see next comment and ffmpeg docs)
    assert(output_filepath != filepath)
    print(filepath)
    video_opts = '-c:v copy' 
    call(['ffmpeg', '-i', filepath,] + ['-af'] + ['areverse'] + ['-c:a'] + ['libmp3lame'] + video_opts.split() + [output_filepath]) # '-c:a libmp3lame' is a mp3 audio 
                                                                                                                                    #codec. see previous comment for moar
    os.remove(filepath)
    return output_filepath

def get_thumbnail(in_filename, path, ttl):
    out_filename = os.path.join(path, str(time.time()) + ".jpg")
    open(out_filename, 'a').close()
    try:
        (
            ffmpeg
            .input(in_filename) #, ss=ttl
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return out_filename
    except ffmpeg.Error as e:
      return None

def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
      return metadata.get('duration').seconds
    else:
      return 0

def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
      return metadata.get("width"), metadata.get("height")
    else:
      return 1280, 720
