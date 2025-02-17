import speech_recognition as sr
import webbrowser
import win32com.client as wincl
import pywhatkit as py
import datetime as dt
from datetime import datetime
import random
import serial
import time
import random
import requests
from groq import Groq
from config import news_apikey
from config import chatbot_apikey
import os

def say(text):
    say = wincl.Dispatch('SAPI.SpVoice')
    say.Speak(text)

def load_convo(filename = 'conversation.txt'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read()
    return ''

def save_convo(convo, filename = 'conversation.txt'):
    with open(filename, 'a') as file:
        file.write(convo + '\n')

def chatbot():
    say("Hello i am your chat bot. You can ask me anything you want.")
    while True:
        convo_history = load_convo()

        user_inp = takeCommand()

        if user_inp == 'exit':
            say('Exiting Chatbot')
            break

        elif user_inp == '':
            continue

        else:
            client = Groq(api_key=chatbot_apikey)
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "This is a conversation history:"
                    },
                    {
                        "role": "user",
                        "content": convo_history
                    },
                    {
                        "role": "user",
                        "content": f"{user_inp}\n"
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            llama_resp = ''

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    llama_resp += chunk.choices[0].delta.content or ""
                    print(chunk.choices[0].delta.content or "", end="")

            say(llama_resp)
            save_convo(f'User: {user_inp}')
            save_convo(f'LLaMA: {llama_resp}')


def takeCommand():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f'User said: {query}')
            return query.lower()
    
    except Exception as e:
        print('Sorry an error caused.')

def takeWakeupCommand():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            return query.lower()
    
    except Exception as e:
        print('Sorry an error caused.')



def rps():
    say('Ok Select one from Rock Paper And Scissors')
    query = takeCommand()
    user_input = query
    comp_input = ['r', 'p', 's']

    comp_sel = random.choice(comp_input)

    if user_input == 'rock':
        print(comp_sel)
        if comp_sel == 'p':
            say("you loose")
        elif comp_sel == 's':
            say('you win')
        else:
            say("its a tie")

    elif user_input == 'paper':
        print(comp_sel)
        if comp_sel == 'r':
            say("you win")
        elif comp_sel == 's':
            say("you loose")
        else:
            say("its a tie")

    else:
        print(comp_sel)
        if comp_sel == 'p':
            say('you win')
        elif comp_sel == 'r':
            say('you loose')
        else:
            say('its a tie')


def sleep():
    while True:
        command = takeWakeupCommand()
        if 'victus' in command:
            say('Yes sir i am Listening')
            break
        else:
            continue


# def play_music(song_path = song_path):
#     pygame.mixer.init()
#     pygame.mixer.music.load(song_path)
#     pygame.mixer.music.play()

def news():

    say('from what region you want news?')
    query = takeCommand()
    reg = {
        'india':'&country=in', 'america':'&country=us', 'usa':'&country=us', 'global':''
    }

    regi = reg[query]
    api_key = news_apikey
    url = f'https://newsapi.org/v2/top-headlines?language=en{regi}&apiKey={api_key}'


    response = requests.get(url)

    if response.status_code == 200:
        news_data = response.json()
    
        if news_data['status'] == 'ok':
            articles = news_data.get('articles', [])
        
            if articles:
                for article in articles:
                    headline = article.get('title')
                    print(headline)
                    say(headline)
            else:
                print("No articles found.")
        else:
            print("Failed to fetch headlines. Status:", news_data['status'])
    else:
        print("Failed to fetch headlines. Status code:", response.status_code)


now = int(datetime.now().strftime("%H"))




if __name__ == '__main__':

    if now < 12:
        say("Good Morning sir, How may i help you?")

    if 17 > now > 12:
        say("Good Afternoon sir, How may i help you?")

    elif 21 > now > 17:
        say("Good Evening sir, How may i help you?")

    elif 24 > now >= 21:
        say("Hello sir its actually late and you should rest, But i am here to help you anytime.")

    games = ['Rock Paper Scissors']

    while True:
        query = takeCommand()

        try:
            if 'open google' in query:
                say('Opening Google.com')
                webbrowser.open('www.google.com')
                sleep()

            elif 'play' in query:
                query = query.replace('play', '')
                say(f'Playing {query}')
                py.playonyt(query)
                sleep()

            elif 'spotify' in query:
                say('Opening Spotify')
                webbrowser.open('https://open.spotify.com')
                sleep()

            elif 'date' in query:
                today = dt.date.today().strftime("%B %d, %Y")
                say(f"Sir it's {today}")
                sleep()

            elif 'game' in query:
                say(f'Ok what game do u wanna play. I know few games such as {games}')
                query = takeCommand().lower()
                if 'rock' in query:
                    rps()

            elif 'news' in query:
                news()
                sleep()

            elif 'chatbot' in query:
                chatbot()

            elif 'red' in query:
                say(f'Changing studio light colour to RED')
                ser = serial.Serial('COM6', 9600, timeout=1)

                def change_color(r, g, b):
                    ser.write(bytes([r, g, b]))  # Send RGB values as bytes to Arduino
                    time.sleep(0.1)  # Add a small delay to ensure data transmission

                time.sleep(2)
                change_color(255, 0, 0) 

                ser.close()  # Close the serial connection when done

            elif 'blue' in query:
                say(f'Changing studio light colour to BLUE')
                ser = serial.Serial('COM6', 9600, timeout=1)

                def change_color(r, g, b):
                    ser.write(bytes([r, g, b]))  # Send RGB values as bytes to Arduino
                    time.sleep(0.1)  # Add a small delay to ensure data transmission

                time.sleep(2)
                change_color(0, 0, 255)

                ser.close()  # Close the serial connection when done

            elif 'green' in query:
                say(f'Changing studio light colour to GREEN')
                ser = serial.Serial('COM6', 9600, timeout=1)

                def change_color(r, g, b):
                    ser.write(bytes([r, g, b]))  # Send RGB values as bytes to Arduino
                    time.sleep(0.3)  # Add a small delay to ensure data transmission

                time.sleep(2)
                change_color(0, 255, 0)

                ser.close()  # Close the serial connection when done

            elif 'random colour' in query:
                say(f'Changing to a random colour')
                ser = serial.Serial('COM6', 9600, timeout=1)

                def change_color(r, g, b):
                    ser.write(bytes([r, g, b]))  # Send RGB values as bytes to Arduino
                    time.sleep(0.1)  # Add a small delay to ensure data transmission

                time.sleep(2)
                ran1 = random.randint(0,255)
                ran2 = random.randint(0,255)
                ran3 = random.randint(0,255)
                change_color(ran1, ran2, ran3)

                ser.close()  # Close the serial connection when done

            elif 'rainbow' in query:
                ser = serial.Serial('COM6', 9600, timeout=1)
                say('Turning on RAINBOW effect.')
                time.sleep(2)
                def trigger_rainbow_effect():
                    ser.write(b'r')  # Send command 'r' to trigger rainbow effect
                trigger_rainbow_effect()
                ser.close()

            elif 'turn off' in query:
                say(f'Turning off studio light')
                ser = serial.Serial('COM6', 9600, timeout=1)

                def change_color(r, g, b):
                    ser.write(bytes([r, g, b]))  # Send RGB values as bytes to Arduino
                    time.sleep(0.1)  # Add a small delay to ensure data transmission

                time.sleep(2)
                change_color(0, 0, 0)

                ser.close()  # Close the serial connection when done





                    

            elif 'quit' in query:
                say("OK Sir")
                os.abort()

            elif 'exit' in query:
                say("OK Sir")
                os.abort()

            elif 'sleep' in query:
                say("OK Sir")
                os.abort()
                
            elif 'leave' in query:
                say("OK Sir")
                os.abort()

        except Exception as e:
            print("Sorry, can you please say that again?...")
            print(e)




        

