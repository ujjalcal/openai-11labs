import gradio as gr
from voicegpt3 import handle_input

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
