import subprocess
import os
import json
import config

import praw
import language_tool_python
import pyttsx3
from elevenlabs import play,save
from elevenlabs.client import ElevenLabs
from aeneas.executetask import ExecuteTask
from aeneas.task import Task

# Requires Python 3.11.0

# This script takes a reddit post url, parses it,
# corrects it, then creates a video along with subtitles
# Makes use of aeneas to align subtitles with audio in video
# All files created get sent to outputs directory


#helper that returns title, user, and body in dict
def get_title_user_and_body(submission: praw.models.Submission) -> dict:
    return {
        "title" : submission.title,
        "user" : submission.author.name,
        "subreddit" : submission.subreddit.display_name,
        "body" : submission.selftext
    }

#helper to return audio file with eleven labs
def get_audio_file_elevenlabs(text: str):
    client = ElevenLabs(
        api_key=config.elevenlabs_api_key 
    )
    audio = client.generate(
        text=text,
        voice="Brian",
        model="eleven_multilingual_v2"
    )
    return audio

#helper to create subtitle map for video
def create_subtitle_map():
    aeneas_task.audio_file_path_absolute = os.path.abspath("outputs/audio.AIFF")
    aeneas_task.text_file_path_absolute = os.path.abspath("outputs/transcript.txt")
    aeneas_task.sync_map_file_path_absolute = os.path.abspath("outputs/subtitle_map.json")

    ExecuteTask(aeneas_task).execute()
    aeneas_task.output_sync_map_file()

#helper to use ffmpeg to create video
def combine_video_audio_subtitles(video_url: str):
    ffmpeg_command = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i" , video_url,
        "-i" , "outputs/audio.AIFF",
        "-vf", "ass=outputs/subtitles.ass",
        #map takes only video stream from 0th idx, audio from 1st idx, -shortest makes output length of shortest input
        "-map", "0:v", 
        "-map", "1:a", 
        "-c:v", "libx264",
        "-c:a", "aac", 
        "-shortest", 
        "outputs/video.mp4",
    ]
    subprocess.run(ffmpeg_command)

# helper to parse json and return a string with events for .ass file
def get_event_string() -> str :
    #load json file
    with open ("outputs/subtitle_map.json", 'r') as file:
        data = json.load(file)
    
    ret_val = ""

    #iterate over all time stamps in aeneas
    for fragment in data["fragments"] :
        # cast to a string, secs are formatted as 00:00
        # and minutes are formated as 00
        beg_min = float(fragment["begin"])//60
        beg_min = f"{int(beg_min):02}"
        beg_sec = float(fragment["begin"])%60
        beg_sec = f"{beg_sec:05.2f}"

        end_min = float(fragment["end"])//60
        end_min = f"{int(end_min):02}"
        end_sec = float(fragment["end"])%60
        end_sec = f"{end_sec:05.2f}"
        
        ret_val+=f"Dialogue: 0:{beg_min}:{beg_sec},0:{end_min}:{end_sec},Default,{fragment['lines'][0]}\n" 

    return(ret_val)

# Create .ass file for subtitles
def write_subtitles():
    script_info="[Script Info]\nPlayResX: 600\nPlayResY: 600\nWrapStyle: 1\n\n"

    script_style="[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, Alignment, Encoding\n"
    script_style+="Style: Default,"+subtitle_font+","+subtitle_size+",&Hffffff,&Hffffff,5,0\n"

    script_events = "[Events]\nFormat: Start, End, Style, Text\n"
    script_events += get_event_string() 
    print(script_events)

    with open("outputs/subtitles.ass", 'w') as ass_file:
        ass_file.write(script_info + script_style + script_events)




#configure praw
reddit = praw.Reddit(
    client_id = config.client_id,
    client_secret = config.client_secret,
    password = config.password,
    username = config.username,
    user_agent = config.user_agent,
)

#configure language_tool
tool = language_tool_python.LanguageTool('en-US')

#configure elevenlabs
client = ElevenLabs(
  api_key=config.elevenlabs_api_key 
)

#configure pyttsx3
engine = pyttsx3.init("nsss")
engine.setProperty('rate', 120)    

#config task obj for aeneas
config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
aeneas_task = Task(config_string=config_string)

#config subtitles (font, size, color, strings)
subtitle_font = "Arial"
subtitle_size = "60"




#get url from user, set as submission, get all relevant info
url: str = input()
submission: praw.models.Submission = reddit.submission(url=url)
post = get_title_user_and_body(submission)

#run language_tool on body
corrected_text = tool.correct(post['body'])
#add line breaks so aeneas givees time stamp for each word
corrected_text = corrected_text.split()
corrected_text = "\n".join(corrected_text)

#concenate all relevant fields of post into one string
transcript = post['title'] + ",\n" + "from r/" + post['subreddit'] + ", by u/" + post['user']
transcript+= ", \n\n" + corrected_text

#write corrected text to txt file
f = open("outputs/transcript.txt", "w")
f.write(transcript)
f.close()

#tts, play, and save with eleven labs
#audio = get_audio_file_elevenlabs(corrected_text)
#play(audio)
#save(audio, "output.mp3")

#tts with pyttsx3
engine.say("a")
engine.save_to_file(transcript, 'outputs/audio.AIFF')
engine.runAndWait()

#use alligner to generate subtitle map with audio
create_subtitle_map()

#generate subtitles
write_subtitles()

#combine video and audio
combine_video_audio_subtitles("../bgVideos/bballBoom.mp4")
