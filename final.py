# final.py

import json
import time
import threading
from transcription_module import record_audio, record_video, transcribe_audio, save_transcription_to_json
from speech_module import read_text_from_json, text_to_speech, play_audio
from pynput import keyboard
import os

# Global events
start_event = threading.Event()
stop_event = threading.Event()

# Directory for storing audio and video files
output_dir = r"C:\Users\ASUS\Desktop\final_AI\output"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def ask_question(question, question_audio_file):
    # Convert the question to speech and play it
    try:
        text_to_speech(question, question_audio_file)
        play_audio(question_audio_file)
    except PermissionError as e:
        print(f"PermissionError: {e}")
    except Exception as e:
        print(f"An error occurred while processing question audio: {e}")
    print(question)

def on_press(key):
    try:
        if key.char == 's':
            stop_event.set()
            print("Stop event set.")
            return False
    except AttributeError:
        pass

def reset_events():
    start_event.clear()
    stop_event.clear()

def main(json_filename):
    # Read the questions from the JSON file
    with open(json_filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    for i, item in enumerate(data):
        question = item.get('question', '')
        if not question:
            print(f"No question found for item {i}. Skipping.")
            continue
        
        question_audio_file = os.path.join(output_dir, f"question_{i}.mp3")
        answer_audio_file = os.path.join(output_dir, f"answer_{i}.wav")
        answer_video_file = os.path.join(output_dir, f"answer_{i}.avi")
        answer_json_file = os.path.join(output_dir, f"answer_{i}.json")
        
        # Reset events for each question
        reset_events()
        
        # Ask the question
        ask_question(question, question_audio_file)
        
        # Prepare for recording the answer
        audio_thread = threading.Thread(target=record_audio, args=(answer_audio_file, start_event, stop_event))
        video_thread = threading.Thread(target=record_video, args=(answer_video_file, start_event, stop_event))
        
        audio_thread.start()
        video_thread.start()
        
        # Wait for both threads to be ready
        time.sleep(2)
        
        # Start both recordings simultaneously
        print("Starting recordings...")
        start_event.set()

        # Wait for 's' key to stop recording
        print("Press 's' to stop recording.")
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        
        # Wait for threads to finish recording
        audio_thread.join()
        video_thread.join()
        
        # Transcribe the recorded audio
        print("Transcribing audio... This may take a while.")
        transcription, error = transcribe_audio(answer_audio_file)
        
        if transcription is not None:
            print("Transcription successful.")
            save_transcription_to_json(transcription, answer_json_file)
        else:
            print(f"Transcription failed for question {i}.")
            if error:
                print(f"Error: {error}")

if __name__ == "__main__":
    json_filename = r"C:\Users\ASUS\Desktop\final_AI\questions.json"  # Replace with your JSON file path
    main(json_filename)
