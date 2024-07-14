import speech_recognition as sr
import webbrowser
import win32com.client as wincl
import pywhatkit as py
import os
import subprocess as sb
import datetime as dt
from datetime import datetime
import serial
import time
import random
import requests

#To convert text to speech:
def say(text):
    say = wincl.Dispatch('SAPI.SpVoice')
    say.Speak(text)

#To take command from user:
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

#Returns news from specified region
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

#Load Dictionaries:
def load_dict_from_file(filename):
    """Read key-value pairs from a file and return as a dictionary."""
    my_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            # Strip whitespace and split by the colon
            key, value = line.strip().split('?')
            my_dict[key] = value
    return my_dict

now = int(datetime.now().strftime("%H"))

#Dictionary for Softwares and sites:
Sites = load_dict_from_file('sites.txt')

Software = load_dict_from_file('software.txt')


if __name__ == '__main__':

    if now < 12:
        say("Good Morning sir, How may i help you?")

    if 17 > now > 12:
        say("Good Afternoon sir, How may i help you?")

    elif 21 > now > 17:
        say("Good Evening sir, How may i help you?")

    elif 24 > now >= 21:
        say("Hello sir its actually late and you should rest, But i am here to help you anytime.")

    
    while True:
        query = takeCommand()

        try:
            #Sites:
            if 'open' in query:
                query = query.replace('open', '')
                query = query.replace('run', '')
                query = query.replace(' ', '')
                if query in Sites:
                    say(f'Opening {query}')
                    webbrowser.open(Sites[query])
                elif query in Software:
                    say(f'Opening {query}')
                    sb.run(Software[query])
                else:
                    say('I dont have the location of specified programm. Tell me is it a site or software')
                    program = takeCommand()
                    try:
                        if program == 'site':
                            say('Ok provide me the link of the site i will add it to my memory')
                            site_link = input('Enter the link of site\n>>')
                            with open('site.txt', 'a') as f:
                                f.write(f'{query}?{site_link}\n')
                            webbrowser.open(f'www.{site_link}.com')
                        elif program == 'software':
                            say('Ok give me the path of the software i will add it to my memory')
                            software_path = input('Enter the path of software with double " \ "\n>>')
                            with open('software.txt', 'a') as f:
                                f.write(f'{query}?{software_path}\n')
                            sb.run(software_path)
                    except Exception as e:
                        print(e)

                    
                


            #Youtube:
            elif 'play' in query:
                query = query.replace('play', '')
                say(f'Playing {query}')
                py.playonyt(query)


            # #Apps:
            # elif 'brave' in query:
            #     say

            

            elif 'date' in query:
                today = dt.date.today().strftime("%B %d, %Y")
                say(f"Sir it's {today}")

            elif 'news' in query:
                news()

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