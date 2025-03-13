import subprocess
import os
import json
import textwrap
import json
from dataclasses import dataclass
import random
from typing import List
import config

import praw
import pyttsx3
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from PIL import Image, ImageDraw, ImageFont
import librosa
from yake import KeywordExtractor
from pyt2s.services import acapela

#Helper Methods

#Used in Generate_Video
#Includes voice commands, audio generation,
#video generator, etc etc


base_dir : str = os.path.dirname(os.path.abspath(__file__))

#helper to list available voices with pytssx3
def list_pytts_voices():
    engine = pyttsx3.init("nsss")

    voices = engine.getProperty('voices')
    for idx, voice in enumerate(voices):
        print(f"Voice #{idx}")
        print(f" - ID: {voice.id}")
        print(f" - Name: {voice.name}")
        print(f" - Languages: {voice.languages}")
        print(f" - Gender: {voice.gender}")
        print(f" - Age: {voice.age}\n")
    return voices


#helper that returns title, user, and body in dict
def get_title_user_and_body(submission: praw.models.Submission) -> dict:
    return {
        "title" : submission.title,
        "user" : submission.author.name if submission.author is not None else "deleted",
        "subreddit" : submission.subreddit.display_name,
        "body" : submission.selftext
    }


#write caption to file 
def generate_caption(text: str, subreddit, output_url: str) -> str:
    tagger = kw_extractor = KeywordExtractor(lan="en")

    #get keywords
    tags: List[str] = [keyword for keyword, score in tagger.extract_keywords(text)]
    
    caption = f"-\nMade With Short-Form Content Creator\nGame: BBall Boom\n#reddit #shorts #story #r #{subreddit} "

    for i in range(len(tags)):
        # want only first 4 tags
        if (i >= 4):
            break
        splitted = tags[i].split()

        #tag per space
        for tag in splitted:
            #make sure no dupes!
            if (tag not in caption):
                caption+= f"#{tag} "
    
    #write into caption file
    with open(output_url, 'w') as f:
        f.write(caption)

#helper to create transcript
def create_body_string(text):
    #add line breaks so aeneas givees time stamp for each word
    text = text.split()
    text = "\n".join(text)

    return text

#helper to create subtitle map for video
def create_subtitle_map(audio_url, text_url, output_url):
    config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
    aeneas_task = Task(config_string=config_string)

    aeneas_task.audio_file_path_absolute = audio_url
    aeneas_task.text_file_path_absolute = text_url
    aeneas_task.sync_map_file_path_absolute = output_url #os.path.join(base_dir, "outputs/subtitle_map.json")

    ExecuteTask(aeneas_task).execute()
    aeneas_task.output_sync_map_file()

#helper to use ffmpeg to create video
def create_video(video_url, video_start, audio_url, subtitle_url):
    reddit_card_url = os.path.join(base_dir,"outputs/reddit_card.png")

    ffmpeg_command = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-ss", video_start,
        "-i" , video_url, 
        "-i" , reddit_card_url, 
        "-i" , audio_url,
        "-filter_complex",
        (
            #add reddit card overlay
            f"[0:v][1:v]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:enable='between(t,0,{end_of_reddit_card})',"
            #add subtitle overlay
            f"ass={subtitle_url};"
            #label audio stream as aud
        ),
        #map takes audio stream from 1st idx, -shortest makes output length of shortest input
        "-map", "2", 
        "-c:v", "libx264",
        "-c:a", "aac", 
        "-aspect", "9:16",
        "-shortest", 
        "-async", "1",
        os.path.join(base_dir,"outputs/video.mp4"),
    ]
    subprocess.run(ffmpeg_command)

# helper to parse json and return a string with events for .ass file
def get_event_string() -> str :

    #load json file
    with open (os.path.join(base_dir, "outputs/subtitle_map.json"), 'r') as file:
        data = json.load(file)
    
    #clear text in first two fragments since they will be replaced
    #with reddit card img
    data["fragments"][0]['lines'][0]=""
    #set end of reddit card time
    global end_of_reddit_card
    end_of_reddit_card = float(data["fragments"][0]['end'])

    ret_val = ""

    #iterate over all time stamps in aeneas
    for fragment in data["fragments"] :
        #add ___ offset to all timestamps for beginning card
        fragment["begin"] = str(float(fragment["begin"]))
        fragment["end"] = str(float(fragment["end"]))

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
def write_subtitles(subtitle_font, subtitle_size, subtitle_color, output_url):
    #set up boiler plate .ass info
    script_info="[Script Info]\nPlayResX: 600\nPlayResY: 600\nWrapStyle: 1\n"

    script_style="[V4+ Styles]\n"
    script_style+="Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, Outline, Outline Colour, Alignment, Encoding\n"
    script_style+=f"Style: Default,{subtitle_font},{subtitle_size},{subtitle_color},&Hffffff,8,&Hffffff,5,0\n"

    script_events = "[Events]\nFormat: Start, End, Style, Text\n"
    #
    #parse transcript map json
    script_events += get_event_string() 
    
    #write .ass file
    with open(output_url, 'w') as ass_file:
        ass_file.write(script_info + script_style + script_events)

# helper to get reddit card
def generate_reddit_card(title, subreddit, user):
    #grab img
    img = Image.open(os.path.join(base_dir,"assets/redditCard.png"))
    draw = ImageDraw.Draw(img)

    #make fonts
    subreddit_font = ImageFont.truetype("/System/Library/Fonts/Static/Inter_24pt-Bold.ttf", 36)
    user_font = ImageFont.truetype("/System/Library/Fonts/Static/Inter_24pt-Bold.ttf", 30)
    title_font = ImageFont.truetype("/System/Library/Fonts/Static/Inter_24pt-Bold.ttf", 40)

    #positions
    header_x = 175
    body_x = 50
    subreddit_y = 40
    user_y = 100
    body_y = 185

    #size
    box_width = 40

    # Add texts to image
    draw.multiline_text( #subreddit
        (header_x,subreddit_y), 
        f"r/{subreddit}", 
        font=subreddit_font, 
        fill="black",
        align="left",
    )
    draw.multiline_text( #user
        (header_x,user_y), 
        f"u/{user}", 
        font=user_font, 
        fill="gray",
        align="left",
    )
    #wrapped text that goes down
    y_offset = body_y
    spacing =  (title_font.getbbox("SSD")[3]-title_font.getbbox("SSD")[1]) + 17
    for line in textwrap.wrap(title, width=box_width):
        draw.text((body_x, y_offset), line, font=title_font, fill="black")
        y_offset += (spacing) + 17

    #save
    img.save(os.path.join(base_dir,"outputs","reddit_card.png"))

    #quick resize
    img = Image.open(os.path.join(base_dir,"outputs","reddit_card.png"))
    img = img.resize((550,300), Image.Resampling.LANCZOS)
    img.save(os.path.join(base_dir,"outputs","reddit_card.png"))

#grab a random place in the gameplay to start from
def get_random_video_start(video_url: str, audio_url) -> str:
    video_file_length = librosa.get_duration(path=video_url)
    audio_length = librosa.get_duration(path=audio_url)

    possible_time_sec : int = random.randint(0,int(video_file_length - audio_length))
    mins = possible_time_sec//60
    mins = f"{mins:02}"
    secs = possible_time_sec%60
    secs = f"{secs:02}"

    return f"00:{mins}:{secs}.0"

#outputs mp3 file of tts with appropriate software
def create_audio(software : str, text: str, save_path: str) -> None :
    #use elevelabs
    if(software == "AI-Powered"):
        #set up client
        client = ElevenLabs(
            api_key=config.elevenlabs_api_key 
        )

        audio = client.generate(
            text=text,
            voice="Brian",
            model="eleven_multilingual_v2",
        )
        save(audio, save_path)

    #use pyt2s
    elif(software == "Medium Quality") :
        data = acapela.requestTTS(text=text, voice='darius22k')
        with open(save_path, 'wb') as file :
            file.write(data)

    #use pytts
    else :
        #configure pyttsx3
        engine = pyttsx3.init("nsss")
        #engine.setProperty('rate')   

        engine.setProperty('voice', 'com.apple.voice.compact.en-GB.Daniel')
        engine.say("a")
        engine.save_to_file(text, save_path)
        engine.runAndWait() 

#concatenate a list of audios together into one file, order of 
#input list matters!
def concatenate_audio(filepaths : List, output_url: str):
    #format input_args
    input_args=[]
    for path in filepaths:
        #create flattened list
        input_args.extend(["-i", path])

    #format the filter_complex, i.e.
    #[0:a:0]...concat=n=?v=0a=1[out]
    filter_complex = "".join(f"[{i}:a]" for i in range(len(filepaths)))
    filter_complex+= f"concat=n={len(filepaths)}:v=0:a=1[out]"

    #create ffmpeg cmd, run it
    command=[
        "ffmpeg", "-y",
        *input_args,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        output_url
    ]
    subprocess.run(command)