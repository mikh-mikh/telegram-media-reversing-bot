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
    # Check file size, if larger than 100MB, split the file
    file_size = os.path.getsize(filepath)
    chunk_size = download_dir * 1024 * 1024  # 30MB in bytes
    if file_size > chunk_size:
        # Split the file into chunks
        chunk_prefix = basefilepath + '_part_'
        call(['ffmpeg', '-i', filepath, '-c', 'copy', '-f', 'segment', '-segment_time', '600', '-reset_timestamps', '1', chunk_prefix + '%03d' + extension])
        
        # Process each chunk
        for filename in os.listdir(os.path.dirname(filepath)):
            if filename.startswith(os.path.basename(basefilepath) + '_part_'):
                video_opts = '-c:v libx264  -vf reverse'  # Add your processing options here

                call(['ffmpeg', '-i', os.path.join(os.path.dirname(filepath), filename)] + ['-af'] + ['areverse'] + video_opts.split() + [os.path.join(os.path.dirname(filepath), 'processed_' + filename)])

        # Concatenate the processed chunks
        with open('files.txt', 'w') as f:
            for filename in sorted(os.listdir(os.path.dirname(filepath)), reverse=True):
                if filename.startswith('processed_' + os.path.basename(basefilepath) + '_part_'):
                    f.write(f"file '{os.path.join(os.path.dirname(filepath), filename)}'\n")
        
        call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'files.txt', '-c', 'copy', output_filepath])
        os.remove('files.txt')  # Clean up temporary files

    else:    
        video_codec = get_codec(filepath, channel='v:0')
        if video_codec == [] :
            video_opts = '' 
        elif video_codec[0] == 'mjpeg'  : # and audio_codec[0] == 'mp3'
            video_opts = '-c:v copy'
        else:
            video_opts = '-c:v libx264  -vf reverse' # -g 125 -qmax 51 -level:v 9.1 -top 1 -threads 8
     
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
