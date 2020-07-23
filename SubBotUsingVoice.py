import requests
from bs4 import BeautifulSoup
import re
import progressbar
import speech_recognition as sr
import pyttsx3
engine = pyttsx3.init()
engine.say("Speak Now")
print("Speak Now")
engine.runAndWait()
r = sr.Recognizer()
rr = sr.Recognizer()
check = False
with sr.Microphone() as source:
    audio = r.listen(source)
try:
    sub = r.recognize_google(audio)
    try:
        print("Did you mean?",sub,".Speak yes/no")
        engine.say("Did you mean"+sub+"?Speak yes or no")
        engine.runAndWait()
    except:
        print("Did you mean",sub,"?Speak yes/no")
    with sr.Microphone() as src:
        n = rr.listen(src)
    nn = rr.recognize_google(n)

    if nn=="no" or nn=="No":
        check = True
        engine = pyttsx3.init()
        print("Ok, please type your movie name! I was unable to recognize correctly.")
        engine.say("Ok, please type your movie name! I was unable to recognize correctly.")
        engine.runAndWait()
        
except:
    engine.say("Sorry couldn't recognize your voice! ")
    engine.runAndWait()
    print("Sorry couldn't recognize your voice! ")
    check = True

if check==True:
        engine.say("Enter the movie name: ")
        engine.runAndWait()
        sub = input("Enter the movie name: ")
lst = list(sub.split(" "))
url = "https://www.google.com/search?q="
find = ""
engine.say("Analysing your query")
engine.runAndWait()
print('----------------------------Analysing your query---------------------------------')
bar = progressbar.ProgressBar(maxval=len(lst), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
count = 0
for i in lst:
    bar.update(count+1)
    url = url+i+"+"
    find += i.capitalize()+" "
bar.finish()
try:
    find += "English subtitle - Subscene"
    url = url + "english+subtitle+subscene"
    google_url_data = requests.get(url, allow_redirects=True)
    soup = BeautifulSoup(google_url_data.text,'html.parser')
    init_links = soup.find_all('a')
    sub_links = []
    find_lst = find.split(" ")
except:
    engine.say("No result found")
    engine.runAndWait()
    print('No result found')
    exit()
engine.say("Searching For All Possible Results")
engine.runAndWait()
print('---------------------Searching For All Possible Results--------------------------');
bar = progressbar.ProgressBar(maxval=len(init_links), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
count = 0
try:
    for link in init_links:
        bar.update(count+1)
        for h3 in link.find_all('h3'):
        	cnt = 0
        	for fi in find_lst:
        		if fi in h3.text:
        			cnt+=1
        	if cnt==len(find_lst):
        		if "Rating" not in h3.text:
        			sub_links.append(link)
        			break
except:
    engine.say("No result found")
    engine.runAndWait()
    print('No result found')
    exit()
bar.finish()

try:
    link = sub_links[0]['href'][7:]
    link = link.split("&")[0]
    subscene_page_data = requests.get(link, allow_redirects=True)
    soup_subscene = BeautifulSoup(subscene_page_data.text,'html.parser')
    final_link = "https://subscene.com"
except:
    engine.say("No result found")
    engine.runAndWait()
    print('No result found')
    exit()
engine.say("Finding and Downloading Best Match")
engine.runAndWait()
print('---------------------Finding and Downloading Best Match--------------------------');
data = soup_subscene.findAll('div',attrs={'class':'download'})
bar = progressbar.ProgressBar(maxval=len(data), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
count = 0

try:
    for div in data:
        bar.update(count+1)
        links = div.findAll('a')
        for a in links:
            final_link+=a['href']
    bar.finish()
    r = requests.get(final_link, allow_redirects=True)
    file = open(find+'.zip', 'wb')
    file.write(r.content)
    engine.say("File is saved as"+file.name)
    engine.runAndWait()
    print('File is saved as ' + file.name)
except:
    engine.say("No Match found",file.name)
    engine.runAndWait()
    print('No Match found')
    exit()
