import gradio as gr
import openai
from elevenlabs import generate, stream, set_api_key
import time

from config import OPENAI_API_KEY, ELEVENLABS_API_KEY

# Set API keys
openai.api_key = OPENAI_API_KEY
set_api_key(ELEVENLABS_API_KEY)

messages = ["You are a freedom mortgage ai assistant. Your name is Harb."]

def gpt3_response(input_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input_text,
        max_tokens=80,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response["choices"][0]["text"]

def audio_stream(text):
    audio_data = generate(
        text=text,
        voice="Bella",
        model="eleven_monolingual_v1",
        stream=True
    )
    stream(audio_data)

def handle_input(audio=None, text_input=None):
    global messages
    
    if audio:
        audio_file = open(audio, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        user_message = transcript['text']
        messages.append(f"User: {user_message}")
        
    if text_input:
        user_message = text_input
        messages.append(f"User: {text_input}")
        
    bot_response = gpt3_response(user_message)
    messages.append(f"Harb: {bot_response}")

    # Stream audio response
    audio_stream(bot_response)

    chat_transcript = "\n\n".join(messages)
    return chat_transcript

iface = gr.Interface(
    fn=handle_input,
    inputs=[
        gr.Audio(source="microphone", type="filepath"),
        gr.Textbox(placeholder="Type your message here...")
    ],
    outputs=gr.Textbox(placeholder="Chat History..."),
    title="🤖 Harb: Your AI Assistant 🤖",
    description="Talk or type to communicate with Harb.",
    live=True
)

iface.launch(height=400)
