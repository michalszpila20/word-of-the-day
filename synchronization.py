import requests

url = "https://raw.githubusercontent.com/michalszpila20/word-of-the-day/master/word_of_the_day.db"

headers = {'User-Agent': 'Mozilla/5.0'}

database_response = requests.get(url, headers=headers)
database_path = "word_of_the_day.db"

if database_response.status_code == 200:
    with open(database_path, 'wb') as file:
        file.write(database_response.content)
    print('Database downloaded successfully')
else:
    print('Failed to download database')