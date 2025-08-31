import requests
from bs4 import BeautifulSoup

url = "https://dictionary.cambridge.org/dictionary/"
basic_url = "https://dictionary.cambridge.org"
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

pretty_soup = soup.prettify()

with open("file1.txt", "w", encoding="utf-8") as f:
    f.writelines(pretty_soup)

for link in soup.find_all('a'):
    
    if "About this" in link:
        print(link) 
        word_url = link.get("href")
        response = requests.get(basic_url + word_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        with open("file2.txt", "w", encoding="utf-8") as f:
            f.writelines(pretty_soup)
