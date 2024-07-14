import speech_recognition as sr
import webbrowser
import win32com.client as wincl
import pywhatkit as py
import os
import subprocess as sb
import datetime as dt
from datetime import datetime
import random 
import pygame
import serial
import time
import random
import requests

def say(text):
    say = wincl.Dispatch('SAPI.SpVoice')
    say.Speak(text)




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

def wakeup():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print('Listening...')
            r.pause_threshold = 1
            audio = r.listen(source)
            query = r.recognize_google(audio, language='en-in')
            return query.lower()
    
    except Exception as e:
        pass


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
            
def wakeup_1():
    n = 1
    while n>0:
        command = wakeup()
        if "victus" in command:
            say('Yes sir i am Listening...')
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
    api_key = 'cb8d3f1f44d34d1e84f8528282ba4471'
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
                wakeup_1()

            elif 'play' in query:
                query = query.replace('play', '')
                say(f'Playing {query}')
                py.playonyt(query)

            elif 'spotify' in query:
                say('Opening Spotify')
                webbrowser.open('https://open.spotify.com')

            elif 'date' in query:
                today = dt.date.today().strftime("%B %d, %Y")
                say(f"Sir it's {today}")

            elif 'game' in query:
                say(f'Ok what game do u wanna play. I know few games such as {games}')
                query = takeCommand().lower()
                if 'rock' in query:
                    rps()

            elif 'news' in query:
                news()

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




        

