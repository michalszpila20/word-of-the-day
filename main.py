import requests
from bs4 import BeautifulSoup
from database import Database

url = "https://dictionary.cambridge.org/dictionary/"
basic_url = "https://dictionary.cambridge.org"
headers = {'User-Agent': 'Mozilla/5.0'}

homepage_response = requests.get(url, headers=headers)

soup_homepage = BeautifulSoup(homepage_response.content, 'html.parser')

pretty_soup = soup_homepage.prettify()

full_link = ""

for link in soup_homepage.find_all('a'):
    
    if "About this" in link:
        word_url = link.get("href")
        full_link = basic_url + word_url

response_word = requests.get(full_link, headers=headers)
soup_word = BeautifulSoup(response_word.content, 'html.parser')
pretty_word = soup_word.prettify()

for text in soup_word.find_all("div", class_="di-title"):
    word = text.getText()
    print(f"word: {word}")
    break

meaning = []
example = []
elements = soup_word.find("div", class_="entry-body").find_all("div", class_="def-block ddef_block")

for element in elements:

    for text in element.find_all("div", class_="def ddef_d db"):
        meaning.append(text.getText().replace(': ', ''))

    tags = element.find_all("span", class_="eg deg")

    mini_example = []

    for tag in tags:
        mini_example.append(tag.getText())

    example.append(mini_example)
    
print(f"meaning: {meaning}")     
print(f"example: {example}")

db = Database()
db.insert(word, str(meaning), str(example))
# # db.delete("renewal")

