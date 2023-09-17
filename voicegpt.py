import gradio as gr
import openai
import winsound

from elevenlabs import generate, stream, set_api_key
from pydub import AudioSegment
from pydub.playback import play
import io
import time 



openai.api_key = "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" #config.OPENAI_API_KEY
api_key = "2d1f8170c1745b6003b59ee3b39de86f" #config.ELEVENLABS_API_KEY
from elevenlabs import set_api_key
set_api_key(api_key)


messages = ["You are an freedom mortgage ai assistant. Your name is Harb. Please respond to all input in 25 words or less."]


def transcribe(audio):
    start_time = time.time()
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    elapsed_time = time.time() - start_time 
    print(f"Whisper Transcription took {elapsed_time} seconds")

    messages.append(f"\nUser: {transcript['text']}")

    start_time = time.time()
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=messages[-1],
        max_tokens=80,
        n=1,
        stop=None,
        temperature=0.5,
    )
    elapsed_time = time.time() - start_time
    print(f"Text Generation took {elapsed_time} seconds")

    system_message = response["choices"][0]["text"]
    messages.append(f"{system_message}")

    ##  Audio Generation with ElevenLabs API ##
    start_time = time.time()
    audio = generate(
        text=system_message,
        voice="Antoni", # "Antoni", "Celia", "Ella", "Ethan", "Harper", "Liam", "Lily", "Mia", "Oliver", "Sophia", "William"
        #emotion="happy", # "neutral", "happy", "sad", "angry"
        latency=4,
        model="eleven_monolingual_v1"
        #optimize_streaming_latency=4
    )
    elapsed_time = time.time() - start_time
    print(f"Audio Generation took {elapsed_time} seconds")

    ## Audio playback with PyDub ##
    audio = AudioSegment.from_file(io.BytesIO(audio), format="mp3")
    audio.export("output.wav", format="wav")

    ## Audio playback with winsound ##
    winsound.PlaySound("output.wav", winsound.SND_FILENAME)

    chat_transcript = "\n".join(messages)
    return chat_transcript

iface = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(source="microphone", type="filepath", placeholder="Please start speaking..."),
    outputs="text",
    title="🤖 My Desktop ChatGPT Assistant 🤖",
    description="🌟 Please ask me your question and I will respond both verbally and in text to you...",
)

iface.launch()
