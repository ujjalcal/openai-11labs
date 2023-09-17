import gradio as gr
import openai
from elevenlabs import generate, stream
from pydub import AudioSegment
from pydub.playback import play
from elevenlabs import generate, stream, set_api_key

import time

from config import OPENAI_API_KEY, ELEVENLABS_API_KEY

# Set API keys
openai.api_key = OPENAI_API_KEY
set_api_key(ELEVENLABS_API_KEY)


messages = ["You are a freedom mortgage ai assistant. Your name is Harb. Please respond to all input in 25 words or less."]

def text_chunks(input_text, chunk_size=25):  # Assuming you want responses in 25 words or less
    words = input_text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i+chunk_size])

def gpt3_streamed_response(input_text):
    for chunk in text_chunks(input_text):
        start_time = time.time()
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk,
            max_tokens=80,
            n=1,
            stop=None,
            temperature=0.5
        )
        elapsed_time = time.time() - start_time
        print(f"Time taken for openai.Completion.create(): {elapsed_time:.2f} seconds.")
        yield response["choices"][0]["text"]

def audio_stream(text):
    return generate(
        text=text,
        voice="Bella",
        model="eleven_monolingual_v1",
        stream=True
    )

def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")
    start_time = time.time()
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    elapsed_time = time.time() - start_time
    print(f"Time taken for openai.Audio.transcribe(): {elapsed_time:.2f} seconds.")
    messages.append(f"\nUser: {transcript['text']}")

    # Get GPT-3 responses in a streaming manner.
    for response_text in gpt3_streamed_response(transcript['text']):
        audio_data = audio_stream(response_text)
        stream(audio_data)
        messages.append(response_text)

    chat_transcript = "\n".join(messages)
    return chat_transcript

# iface = gr.Interface(
#     fn=transcribe,
#     inputs=gr.Audio(source="microphone", type="filepath", placeholder="Please start speaking..."),
#     outputs="text",
#     title="🤖 My Desktop ChatGPT Assistant 🤖",
#     description="🌟 Please ask me your question and I will respond both verbally and in text to you...",
# )


iface = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(source="microphone", type="filepath", placeholder="Please start speaking...", duration=10),  # duration can be set to a max value you think will be reasonable for the user to hold down the button.
    outputs="text",
    title="🤖 My Desktop ChatGPT Assistant 🤖",
    description="🌟 Please ask me your question and I will respond both verbally and in text to you...",
    live=True  # This makes the interface live, automatically processing the input as it changes.
)

iface.launch()


iface.launch()
