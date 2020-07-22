import requests
from bs4 import BeautifulSoup
import re
sub = input("Enter the movie name: ")
lst = list(sub.split(" "))
url = "https://www.google.com/search?q="
find = ""
for i in lst:
    url = url+i+"+"
    find += i.capitalize()+" "
find += "English subtitle - Subscene"
find_lst = find.split(" ")
url = url + "english+subtitle+subscene"
google_url_data = requests.get(url, allow_redirects=True)
soup = BeautifulSoup(google_url_data.text,'html.parser')
init_links = soup.find_all('a')
sub_links = []

for link in init_links:
	for h3 in link.find_all('h3'):
		cnt=0
		for fi in find_lst:
			if fi in h3.text:
				cnt+=1
		if cnt==len(find_lst):
			if "Rating" not in h3.text:
				sub_links.append(link)
				break

link = sub_links[0]['href'][7:]
link = link.split("&")[0]
subscene_page_data = requests.get(link, allow_redirects=True)
soup_subscene = BeautifulSoup(subscene_page_data.text,'html.parser')
final_link = "https://subscene.com"
data = soup_subscene.findAll('div',attrs={'class':'download'})
for div in data:
    links = div.findAll('a')
    for a in links:
        final_link+=a['href']

r = requests.get(final_link, allow_redirects=True)
open(find+'.zip', 'wb').write(r.content)
print("Downloaded Successfully!")