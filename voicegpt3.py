import pyaudio
import numpy as np
import openai
import time
from elevenlabs import generate, stream, set_api_key
from config import OPENAI_API_KEY, ELEVENLABS_API_KEY

# Set API keys
openai.api_key = OPENAI_API_KEY
set_api_key(ELEVENLABS_API_KEY)

# Audio Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
THRESHOLD = 200

audio = pyaudio.PyAudio()
messages = ["You are a freedom mortgage ai assistant. Your name is Harb. Please respond to all input in 25 words or less."]


def transcribe(audio_data):
    global messages

    transcript = openai.Audio.transcribe("whisper-1", audio_data)
    messages.append(f"\nUser: {transcript['text']}")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=transcript['text'],
        max_tokens=80,
        n=1,
        stop=None,
        temperature=0.5
    )
    
    response_text = response["choices"][0]["text"]
    messages.append(response_text)
    
    audio_stream_data = generate(
        text=response_text,
        voice="Bella",
        model="eleven_monolingual_v1",
        stream=True
    )
    
    stream(audio_stream_data)
    
    chat_transcript = "\n".join(messages)
    return chat_transcript

def process_audio(audio_data):
    result = transcribe(audio_data)
    print(result)

def listen_continuous(callback):
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Listening...")
    try:
        while True:
            data = stream.read(CHUNK)
            rms = np.sqrt(np.mean(np.square(np.frombuffer(data, dtype=np.int16))))
            #print("RMS:", rms)
            if rms > THRESHOLD:
                print("Heard something!")
                frames = []
                for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                    frames.append(stream.read(CHUNK))
                audio_data = b''.join(frames)
                callback(audio_data)
                time.sleep(RECORD_SECONDS)
    except KeyboardInterrupt:
        print("Interrupted. Closing stream and terminating audio.")
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    listen_continuous(process_audio)
