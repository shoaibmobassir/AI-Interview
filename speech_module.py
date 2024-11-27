# speech_module.py

import json
from gtts import gTTS
import pygame
import time

def read_text_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        # Assuming the JSON file has a key "text" which contains the text to be converted to speech
        if isinstance(data, list):  # If the JSON is a list of segments
            text = ' '.join(segment['text'] for segment in data)
        else:
            text = data.get('text', '')
    return text

def text_to_speech(text, output_audio_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_audio_file)
    print(f"Audio saved to {output_audio_file}")

def play_audio(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)  # Wait until the audio is finished playing

def process_text_to_speech_and_play(json_filename, output_audio_file):
    # Read text from JSON file
    text = read_text_from_json(json_filename)
    
    if text:
        # Convert text to speech and save it
        text_to_speech(text, output_audio_file)
        # Play the saved audio file
        play_audio(output_audio_file)
    else:
        print("No text found in the JSON file.")
