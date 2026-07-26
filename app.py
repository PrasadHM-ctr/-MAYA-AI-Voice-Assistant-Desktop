import os
import threading
import time
import pyautogui
import pywhatkit
import requests
import speech_recognition as sr
import pyttsx3
import datetime
from google import genai
import keyboard
import screen_brightness_control as sbc
import winshell
from send2trash import send2trash
import ctypes
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, request, jsonify
update_status = None
add_message = None

app = Flask(__name__)
speech_lock = threading.Lock()

reminder_active = False
reminder_message = ""
last_reminder_time = 0
FOLDERS = {
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
    "videos": os.path.join(os.path.expanduser("~"), "Videos"),
    "music": os.path.join(os.path.expanduser("~"), "Music")
}

appss=["calculator","notepad"]

client = genai.Client(api_key="AQ.Ab8RN6J2i-PBLIKA83o7499FT14PAGq4p-knGmUG2UTHuXi_FA")
# -----------------------------
# Function: Speak
# -----------------------------
EMAIL = "prasadcloud997@gmail.com"
APP_PASSWORD = "uyws dwra jicm yhaf"
contacts = {
    
    "hello": "+91xxxxxxxxxx",
    "prasad": "+91xxxxxxxxxx",
    
}



# ---------------------------------------------- #
def send_whatsapp():

    speak("Whom do you want to send the message to?")
    name = listen().lower()

    if name not in contacts:
        speak("Contact not found.")
        return

    speak("What message should I send?")
    message = listen()

    pywhatkit.sendwhatmsg_instantly(
        phone_no=contacts[name],
        message=message,
        wait_time=15,
        tab_close=False
    )

    time.sleep(5)
    pyautogui.press("enter")

    speak("Message sent successfully.")

def voice():

    def voice():

      data = request.get_json()
      command = data["message"].lower()

      print(command)

      if "hello" in command:
        reply = "Hello! How can I help you?"

      elif "time" in command:
        reply = "The current time is " + datetime.datetime.now().strftime("%I:%M %p")

      elif "date" in command:
        reply = "Today is " + datetime.datetime.now().strftime("%d %B %Y")

      elif "weather" in command:

         city = command.replace("weather", "").replace("in", "").strip()

         if city:
            get_weather(city)
            reply = (f"Getting weather for {city}")
         else:
            reply = "Please tell the city name."

      else:
        reply = "Sorry, I don't know this command."

      return jsonify({"reply": reply})   

def send_email(receiver, subject, body):

    try:
        speak("Please type the recipient email address.")
        receiver = input("Recipient Email: ").strip()

        speak("Tell me the subject.")
        subject = listen()

        while not subject:
            speak("I didn't understand. Please say the subject again.")
            subject = listen()

        speak("Tell me the message.")
        body = listen()

        while not body:
            speak("I didn't understand. Please say the message again.")
            body = listen()

        message = MIMEMultipart()
        message["From"] = EMAIL
        message["To"] = receiver
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(EMAIL, APP_PASSWORD)

        server.sendmail(
            EMAIL,
            receiver,
            message.as_string()
        )

        server.quit()

        speak("Email sent successfully.")

    except Exception as e:
        print("Error:", e)
        speak("Unable to send email.")
def speak(text):
    with speech_lock:

        print("Assistant:", text)

        if add_message:
            add_message("🤖 MAYA", text)

        if update_status:
            update_status("🗣️ Speaking...")

        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()

        if update_status:
            update_status("✅ Ready")
    


# -----------------------------
# Speech Recognizer
# -----------------------------
recognizer = sr.Recognizer()
recognizer.energy_threshold = 500
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8


# -----------------------------
# Function: Listen
# -----------------------------
def ask_ai(question):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",   # You can also use gemini-flash-latest
            contents=question
        )

        answer = response.text

        print("AI:", answer)
        speak(answer)

    except Exception as e:
        print("Error:", e)
        speak("Sorry, I couldn't connect to Gemini.")
def close_app():

    speak("Which application should I close?")

    app = listen().lower()

    apps = {
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe",
        "chrome": "chrome.exe",
        "paint": "mspaint.exe",
        "edge": "msedge.exe",
        "vscode": "Code.exe",
        "whatsapp": "WhatsApp.exe"
    }

    if app in apps:
        os.system(f'taskkill /f /im "{apps[app]}"')
        speak(f"{app} closed.")
    else:
        speak("Application not found.")       

def listen():

    with sr.Microphone(device_index=1) as source:

        if update_status:
            update_status("⏳ Stay silent for 2 seconds...")
        else:
            print("\nStay silent for 2 seconds...")

        recognizer.adjust_for_ambient_noise(source, duration=2)

        if update_status:
            update_status("🎤 Speak now...")
        else:
            print("Speak now...")

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

            if update_status:
                update_status("🤔 Recognizing...")

            command = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            command = command.lower().strip()

            if update_status:
                update_status(f"✅ You said: {command}")

            print("You said:", command)
            if add_message:
              add_message("🧑 You", command)

            return command

        except sr.WaitTimeoutError:

            if update_status:
                update_status("❌ No speech detected.")
            else:
                print("No speech detected.")

            return ""

        except sr.UnknownValueError:

            if update_status:
                update_status("❌ Could not understand.")
            else:
                print("Sorry, I could not understand.")

            speak("Sorry, I could not understand.")
            return ""

        except sr.RequestError:

            if update_status:
                update_status("🌐 Internet connection error.")
            else:
                print("Please check your internet connection.")

            speak("Please check your internet connection.")
            return ""

API_KEY = "ca3dae65116486129c05ee72344f8c20"

def get_weather(city):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:

        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]

        speak(
            f"The temperature in {city} is {temperature} degree Celsius "
            f"with {description}."
        )

    else:

        speak("City not found.")

def reminder(reminder_time, message):

    reminder_time = datetime.datetime.strptime(reminder_time, "%I:%M %p")
def reminder(reminder_time, message):

    print("Reminder thread started")

    while True:

        current = datetime.datetime.now().strftime("%I:%M %p")

        print("Current:", current, "| Reminder:", reminder_time)

        if current == reminder_time:
            print("Matched!")
            speak(f"Reminder! {message}")
            break

        time.sleep(1)
   
# Welcome Message
# -----------------------------
speak("Hello! I am your voice assistant.")
def take_screenshot():

    try:

        folder = "Screenshots"

        os.makedirs(folder, exist_ok=True)

        filename = datetime.datetime.now().strftime("Screenshot_%Y%m%d_%H%M%S.png")

        path = os.path.join(folder, filename)

        screenshot = pyautogui.screenshot()

        screenshot.save(path)

        speak("Screenshot taken successfully.")

        print("Saved:", path)

    except Exception as e:

        print(e)

        speak("Unable to take screenshot.")

def format_time(spoken_time):

    spoken_time = spoken_time.upper()

    spoken_time = spoken_time.replace(".", "")
    spoken_time = spoken_time.replace(" ", "")

    # Remove any colon spoken by speech recognition
    spoken_time = spoken_time.replace(":", "")

    if spoken_time.endswith("AM") or spoken_time.endswith("PM"):

        period = spoken_time[-2:]
        numbers = spoken_time[:-2]

        if len(numbers) == 3:
            hour = "0" + numbers[0]
            minute = numbers[1:]

        elif len(numbers) == 4:
            hour = numbers[:2]
            minute = numbers[2:]

        else:
            return None

        return f"{hour}:{minute} {period}"

    return None
# -----------------------------
# def start_maya():Main Loop
# -----------------------------
def start_maya():
  while True:

    command = listen()

    if command == "":

        continue

    

    # Hello
    if "hello" in command:
        speak("Hello! How can I help you?")

    # Time
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    # Date
    elif "date" in command:
        today = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today is {today}")

    # Google Search
    elif "search" in command:

        topic = command.replace("search", "").strip()

        if topic:
            speak(f"Searching Google for {topic}")
            webbrowser.open(f"https://www.google.com/search?q={topic}")
        else:
            speak("Please tell me what you want to search.")

    elif "play" in command:

         song = command.replace("play", "").strip()

         if song:
            speak(f"Playing {song} on YouTube")

            pywhatkit.playonyt(song)

         else:
            speak("Please tell me what you want to play.")  
          
    elif command.startswith("open"):

         website = command.replace("open", "").strip()

         if website in appss: 
          
          speak(f"Opening {website}")
          os.startfile (f"{website}")

         
         elif website:
                  speak(f"Opening {website}")
                  webbrowser.open(f"https://www.{website}.com/")   

         else:
              speak("Sorry, I don't know how to open that.")          
    elif "weather" in command:

       city = command.replace("weather", "").replace("in", "").strip()

       if city:

        get_weather(city)

       else:

        speak("Please tell me the city name.")

    elif "set reminder" in command:

         message = command.replace("set reminder", "").strip()

         speak("Tell me the reminder time.")

         reminder_time = listen()

         reminder_time = format_time(reminder_time)

         if reminder_time:

          speak(f"Reminder set for {reminder_time}")

          thread = threading.Thread(
            target=reminder,
            args=(reminder_time, message),
            daemon=True
        )

          thread.start()
    elif "close app" in command:

     close_app()
    
    elif "send whatsapp" in command or "whatsapp message" in command:
           send_whatsapp()
    elif "what" in command:

        question = command.replace("what", "").strip()

        ask_ai(question)    
    elif "take screenshot" in command or "screenshot" in command:

       speak("Taking screenshot.")

       time.sleep(1)

       take_screenshot()    
    elif command.startswith("open folder"):

         folder = command.replace("open folder","").strip()

         if folder in FOLDERS:
            os.startfile(FOLDERS[folder])
            speak(f"Opening {folder}")

         else:
          speak("Folder not found") 
    elif command.startswith("open file"):

        filepath = command.replace("open file","").strip()

        try:
           os.startfile(filepath)
           speak("Opening file")
        except:
         speak("File not found") 
    elif "increase volume" in command:

       for i in range(1):
        keyboard.press_and_release("volume up")

        speak("Volume increased")       
    elif "decrease volume" in command:

      for i in range(1):
        keyboard.press_and_release("volume down")

        speak("Volume decreased")        
    elif "mute volume" in command:

         keyboard.press_and_release("volume mute")

         speak("Volume muted")      
    elif "unmute volume" in command:

         keyboard.press_and_release("volume mute")

         speak("Volume unmuted")      
    elif "increase brightness" in command:

          current = sbc.get_brightness()[0]

          sbc.set_brightness(min(current+20,100))

          speak("Brightness increased")    
    elif "decrease brightness" in command:

        current = sbc.get_brightness()[0]

        sbc.set_brightness(max(current-20,0))

        speak("Brightness decreased")    
    elif "empty recycle bin" in command:

       winshell.recycle_bin().empty(confirm=False,show_progress=False,sound=True)

       speak("Recycle Bin emptied")       
    elif "send email" in command:

      speak("Tell me the recipient email address.")

      receiver = listen().replace(" ", "").lower()
   
      speak("Tell me the subject.")

      subject = listen()

      speak("Tell me the message.")

      body = listen()

      send_email(receiver, subject, body)   
    

    elif "exit" in command or "stop" in command or "bye" in command:
        speak("Goodbye! Have a great day.")
        break

    # Unknown Command
    else:
        speak("Sorry, I don't know this command.")
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/voice", methods=["POST"])
def voice():
    from flask import request, jsonify

    data = request.get_json()

    command = data["message"]

    print(command)

    return jsonify({
        "reply": "You said: " + command
    })


if __name__ == "__main__":

    maya_thread = threading.Thread(target=start_maya, daemon=True)
    maya_thread.start()

    app.run(debug=True, use_reloader=False)