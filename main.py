import requests
import os
from supabase import create_client, Client
from bs4 import BeautifulSoup
from database import Database

url = "https://dictionary.cambridge.org/dictionary/"
basic_url = "https://dictionary.cambridge.org"
headers = {'User-Agent': 'Mozilla/5.0'}

homepage_response = requests.get(url, headers=headers)

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

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
    break

meaning = []
example = []

if soup_word.find("div", class_= "pr idiom-block"):
    elements = soup_word.find("div", class_="idiom-block").find_all("div", class_="def-block ddef_block")
else:
    elements = soup_word.find("div", class_="entry-body").find_all("div", class_="def-block ddef_block")

for element in elements:

    for text in element.find_all("div", class_="def ddef_d db"):
        meaning.append(text.getText().replace(': ', ''))

    tags = element.find_all("div", class_="examp dexamp")

    mini_example = []
    connotation = ""

    for tag in tags:

        if tag.find("span", class_="lu dlu"):
            connotation = tag.find("span", class_="lu dlu").get_text()
        elif tag.find("a", class_="lu dlu"):
            connotation = tag.find("a", class_="lu dlu").get_text()

        if connotation:
            mini_example.append("(" + str(connotation) + ") - " + tag.find("span", class_="eg deg").get_text())
        else:
            mini_example.append(tag.find("span", class_="eg deg").get_text())

    example.append(mini_example)

response = (
    supabase.table("words")
    .insert(
        {
         "word": word,
         "meaning": str(meaning),
         "example": str(example)
         })
    .execute()
)