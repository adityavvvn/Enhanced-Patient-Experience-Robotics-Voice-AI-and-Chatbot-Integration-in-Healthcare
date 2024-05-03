import tkinter as tk
from PIL import ImageTk, Image
import openai
import pyttsx3
import speech_recognition as sr
import keyboard
import webbrowser

# Set your OpenAI API key
openai.api_key = "sk-proj-bXeXRjVkzLviRiq50O3YT3BlbkFJ0ilgeJ3rU5D5fTFZS2LD"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer() 
    with sr.AudioFile(filename) as source: 
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        print('Skipping due to unknown error:', e)

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You: " + prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def VOICEGPT():
    recording = False  # Flag to indicate whether recording is in progress
    while True:
        print("Say 'Friday' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if transcription.lower() == "friday":
                print("Recording started. Say your question...")
                recording = True  # Set flag to indicate recording started
        except Exception as e:
            print("An error occurred:", e)

        if recording:
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                recognizer.pause_threshold = 1
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
            filename = "input.wav"
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
            # Transcribe audio to text
            text = transcribe_audio_to_text(filename)
            if text:
                print(f"You said: {text}")
                # Generate response using GPT-3
                response = generate_response(text)
                print(f"GPT-3 says: {response}")
                # Read response using text-to-speech
                speak_text(response)
                
                # Check if the specific word is in the response
                if any(word in text.lower() for word in ['having', 'suffering', 'facing', 'booking', 'op', 'emergency']):
                    webbrowser.open("file:///C:/Users/adity/Downloads/robotics/robotics/Sample_rob.html")  # Change the URL to the desired website

            recording = False  # Reset flag after processing the question
            
        # Check if spacebar is pressed to stop the code
        

def CHATGPT():
    import gradio as gr

    initial_message = "You are chatting with a medical AI. Feel free to ask any medical-related questions!"

    def chatbot(input_text):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": initial_message},
                    {"role": "user", "content": input_text}
                ]
            )
            reply = response.choices[0].message['content'].strip()
            return reply
        except Exception as e:
            return str(e)

    def submit_message(input_text):
        return chatbot(input_text)

    def launch_gradio_interface():
        iface = gr.Interface(
            fn=submit_message,
            inputs=gr.Textbox(initial_message, label="Enter your medical question here:", lines=5, placeholder="Type your question here..."),
            outputs=gr.Textbox(label="AI's Reply:", lines=5, placeholder="AI's response will appear here..."),
            title="Medical Chatbot",
            description="Ask the AI any medical-related question",
            theme="huggingface",
            examples=[
                ["What are the symptoms of COVID-19?", "The common symptoms of COVID-19 include fever, cough, and shortness of breath."],
                ["What is diabetes?", "Diabetes is a chronic condition that affects how your body uses blood sugar."]
            ]
        )
        iface.launch()

    launch_gradio_interface()

# Create the main window
root = tk.Tk()
root.title("GPT GUI")
root.geometry("200x200")  # Set the size of the window

# Load background image
bg_image = Image.open("new\Background.jpg")
bg_image = bg_image.resize((800, 600))
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def chatgpt_clicked():
    VOICEGPT()

def medical_chatbot_clicked():
    CHATGPT()

def exit_application():
    root.destroy()

# Add VOICEGPT button
chatgpt_button = tk.Button(root, text="VOICEGPT", command=chatgpt_clicked, width=20, height=2)
chatgpt_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

# Add CHATGPT button
medical_chatbot_button = tk.Button(root, text="CHATGPT", command=medical_chatbot_clicked, width=20, height=2)
medical_chatbot_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Add exit button
exit_button = tk.Button(root, text="Exit", command=exit_application, width=10, height=2)
exit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

root.mainloop()
