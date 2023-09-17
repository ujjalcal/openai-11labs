import gradio as gr
import openai
import winsound
#from elevenlabslib import 
from elevenlabs import generate, play, set_api_key
from pydub import AudioSegment
from pydub.playback import play
import io
#import config

openai.api_key = "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" #config.OPENAI_API_KEY
api_key = "2d1f8170c1745b6003b59ee3b39de86f" #config.ELEVENLABS_API_KEY
from elevenlabslib import ElevenLabsUser
user = ElevenLabsUser(api_key)

messages = ["You are an freedom mortgage ai assistant. Your name is Harb. Please respond to all input in 25 words or less."]

def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append(f"\nUser: {transcript['text']}")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=messages[-1],
        max_tokens=80,
        n=1,
        stop=None,
        temperature=0.5,
    )

    system_message = response["choices"][0]["text"]
    messages.append(f"{system_message}")

    #voice = user.get_voices_by_name("Antoni")[0]
    #audio = generate(system_message, ) #    generate_audio_bytes(system_message)
    audio = generate(
        text=system_message,
        voice="Bella"
    )

    #play(audio, notebook=True)

    audio = AudioSegment.from_file(io.BytesIO(audio), format="mp3")
    audio.export("output.wav", format="wav")

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
