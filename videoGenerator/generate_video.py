import subprocess
import praw
import config
import language_tool_python

from elevenlabs import play,save
from elevenlabs.client import ElevenLabs

import pyttsx3

from aeneas.executetask import ExecuteTask
from aeneas.task import Task


#helper that returns title, user, and body in dict
def get_title_user_and_body(submission: praw.models.Submission) -> dict:
    return {
        "title" : submission.title,
        "user" : submission.author,
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
def create_subtitle_map() -> str:
    aeneas_task.audio_file_path = "audio.AIFF"
    aeneas_task.text_file_path = "transcript.txt"
    aeneas_task.subtitle_map_path = "subtitle_map.json"
    return "wiener"

#helper to use ffmpeg to create video
def combine_video_audio_subtitles(video_url: str):
    ffmpeg_command = [
        "ffmpeg", "-y",
        "-i" , video_url,
        "-i" , "audio.AIFF",
        #map takes only video stream from 0th idx, audio from 1st idx, -shortest makes output length of shortest input
        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-shortest", 
        "output.mp4",
    ]
    subprocess.run(ffmpeg_command)




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
engine.setProperty('rate', 100)    

#create task obj for aeneas
config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
aeneas_task = Task(config_string=config_string)




#get url from user, set as submission, get all relevant info
url: str = input()
submission: praw.models.Submission = reddit.submission(url=url)
post = get_title_user_and_body(submission)

#run language_tool on body
corrected_text = tool.correct(post['body'])
print(corrected_text)

#tts, play, and save with eleven labs
#audio = get_audio_file_elevenlabs(corrected_text)
#play(audio)
#save(audio, "output.mp3")

#tts with pyttsx3
engine.say("a")
engine.save_to_file(corrected_text, 'audio.AIFF')
engine.runAndWait()

#combine video and audio
combine_video_audio_subtitles("../bgVideos/bballBoom.mp4")
