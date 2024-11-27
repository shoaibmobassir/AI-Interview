# transcription_module.py

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
from faster_whisper import WhisperModel
from pynput import keyboard
import threading
import traceback
import os
import json
import cv2
import time

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Initialize the WhisperModel with CPU
model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Global variables
audio_buffer = []
audio_recording = False
video_recording = False

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_buffer.append(indata.copy())

def record_audio(filename, start_event, stop_event, samplerate=16000):
    global audio_recording
    audio_buffer.clear()
    audio_recording = True

    with sd.InputStream(callback=audio_callback, channels=1, dtype='float32', samplerate=samplerate):
        print("Audio stream ready.")
        start_event.wait()
        print("Recording audio... Press 's' to stop.")
        stop_event.wait()
    
    print("Audio recording finished.")
    if audio_buffer:
        audio_data = np.concatenate(audio_buffer, axis=0)
        wavfile.write(filename, samplerate, audio_data)
        print(f"Audio saved to {filename}")
    else:
        print("No audio data recorded.")

def record_video(filename, start_event, stop_event):
    global video_recording
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (frame_width, frame_height))

    video_recording = True
    print("Video stream ready.")
    start_event.wait()
    print("Recording video... Press 's' to stop.")

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        out.write(frame)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved to {filename}")

def transcribe_audio(filename):
    try:
        segments, info = model.transcribe(filename, beam_size=5)
        return [{"start": segment.start, "end": segment.end, "text": segment.text} for segment in segments], None
    except Exception as e:
        return None, e

def save_transcription_to_json(transcription, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(transcription, json_file, ensure_ascii=False, indent=4)
    print(f"Transcription saved to {filename}")

def on_press(key, stop_event):
    try:
        if key.char == 's':
            stop_event.set()
            print("Stop event set.")
            return False
    except AttributeError:
        pass

def record_and_transcribe(start_event, stop_event):
    audio_filename = "recorded_audio.wav"
    video_filename = "recorded_video.avi"
    
    audio_thread = threading.Thread(target=record_audio, args=(audio_filename, start_event, stop_event))
    video_thread = threading.Thread(target=record_video, args=(video_filename, start_event, stop_event))

    audio_thread.start()
    video_thread.start()

    # Wait for both threads to be ready
    time.sleep(2)

    # Start both recordings simultaneously
    start_event.set()

    # Start listener for stopping recording
    with keyboard.Listener(on_press=lambda key: on_press(key, stop_event)) as listener:
        listener.join()

    # Wait for threads to finish recording
    audio_thread.join()
    video_thread.join()

    # Transcribe the recorded audio
    try:
        print("Transcribing audio... This may take a while.")
        transcription, error = transcribe_audio(audio_filename)

        if transcription is not None:
            print("Transcription:")
            for segment in transcription:
                print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")
            
            json_filename = "transcription.json"
            # Print transcription in JSON format
            print(json.dumps(transcription, ensure_ascii=False, indent=4))
            save_transcription_to_json(transcription, json_filename)
        else:
            print("Transcription failed.")
            if error:
                print(f"Error: {error}")
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}")
