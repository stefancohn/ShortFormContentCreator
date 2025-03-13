import os
import json
import sys
import json
from dataclasses import dataclass
import random
from typing import List
import config
from helper_methods import *

import praw
import language_tool_python
import pyttsx3
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from PIL import Image, ImageDraw, ImageFont
import librosa
from yake import KeywordExtractor
from pyt2s.services import acapela

# Requires Python 3.11.0

# This script takes a reddit post url, parses it,
# corrects it, then creates a video along with subtitles
# Makes use of aeneas to align subtitles with audio in video
# All files created get sent to outputs directory
    

#the base dir so this works across everything
base_dir : str = os.path.dirname(os.path.abspath(__file__))

video_url : str = os.path.join(base_dir,"assets/bgVideos/bballBoom2.mp4")
tts_audio_url : str = os.path.join(base_dir,"outputs/tts_audio.wav")
final_audio_url : str = os.path.join(base_dir, "outputs/final_audio.wav")
caption_url : str = os.path.join(base_dir,"outputs/caption.txt")
subtitle_url : str = os.path.join(base_dir,"outputs/subtitles.ass")
reddit_card_url: str = os.path.join(base_dir,"outputs/reddit_card.png")
output_video_url : str = os.path.join(base_dir, "outputs/video.mp4")
ding_audio_url: str = os.path.join(base_dir, "assets/ding.mp3")

#config subtitles (font, size, color, strings)
subtitle_font = "Phosphate"
subtitle_size = "30"
subtitle_color = "&HFDB5A3"

end_of_reddit_card = None
tts_audio_length = 0

#get options, and set up proper vars
options = json.loads(sys.argv[2])
voice_rate = int(options.get('Voice Rate (1-250)', "125"))
tts_software = options.get('Voice Software',"")
parts = int(options.get('Number of Parts',))


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


#get url from user, set as submission, get all relevant info
url: str = sys.argv[1]
submission: praw.models.Submission = reddit.submission(url=url)
post = get_title_user_and_body(submission)

generate_reddit_card(title=post['title'], subreddit=post['subreddit'], user=post['user'])

#run language_tool on body
corrected_text = tool.correct(post['body'])
corrected_text = create_body_string(corrected_text)

#concenate all relevant fields of post into one string
transcript = post['title'] + ",,\n\n"
transcript+= corrected_text

#write corrected text to txt file
f = open(os.path.join(base_dir, "outputs/transcript.txt"), "w")
f.write(transcript)
f.close()

#generate a caption based on keywords of text
generate_caption(text=transcript, subreddit=post['subreddit'], output_url=caption_url)

if (parts == 1) :
    #create audio, concat with ding, get length of audio
    create_audio(software=tts_software, text=transcript, save_path=tts_audio_url)
    concatenate_audio([ding_audio_url, tts_audio_url], final_audio_url)

    #get random time to start video for variance using length of audio
    time_start : str = get_random_video_start(video_url=video_url, audio_url=final_audio_url) 

    #use alligner to generate subtitle map with audio 
    create_subtitle_map(
        audio_url = final_audio_url, 
        text_url = os.path.join(base_dir, "outputs/transcript.txt"), 
        output_url = os.path.join(base_dir, "outputs/subtitle_map.json")
    )

    #generate subtitles and set end of reddit card
    write_subtitles(subtitle_font, subtitle_size, subtitle_color, output_url = subtitle_url)

    #combine video and audio and subs
    create_video(
        video_url = video_url, 
        video_start = time_start,
        audio_url = final_audio_url,
        subtitle_url = subtitle_url
    )

# have a diff process if video splitting
else :

    #record n save tts of "follow for i"
    for i in range(0, parts-1):
        follow_save_url : str = os.path.join(base_dir,f"outputs/follow{i}.wav")
        sequel_text = f"Follow for part {i+2}"
        create_audio(software = tts_software, text = sequel_text, save_path = follow_save_url)

    title_audio_url = os.path.join(base_dir,"outputs/title_audio.wav")
    #record just the title part
    create_audio(tts_software, post['title'], title_audio_url)

    #now we must find out stop points
    #once we find stop point, store it 
    stop_points = []
    corrected_text = corrected_text.split()
    stop_point = int(len(corrected_text)/parts)
    for i in range(0, parts-1):
        while (True):
            #must find natural stop; when we find period
            if "." in corrected_text[stop_point*(i+1)]:
                stop_points.append(stop_point)
                break
            else:
                if stop_point < len(corrected_text):
                    stop_point += 1
                else:
                    exit(0)