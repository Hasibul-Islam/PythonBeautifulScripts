import requests
from bs4 import BeautifulSoup
import re
import progressbar


sub = input("Enter the movie name: ")
lst = list(sub.split(" "))
url = "https://www.google.com/search?q="
find = ""

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
except:
    print('No result found')
    exit()

print('---------------------Searching For All Possible Results--------------------------');
bar = progressbar.ProgressBar(maxval=len(init_links), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
count = 0

try:
    for link in init_links:
        bar.update(count+1)
        for h3 in link.find_all('h3'):
            if find in h3.text and "Ratings" not in h3.text:
                sub_links.append(link)
                break
except:
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
    print('No result found')
    exit()

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
    print('File is saved at ' + file.name)
except:
    print('No Match found')
    exit()