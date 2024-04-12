import requests
import re  
from bs4 import BeautifulSoup  


def get_url():
    for count in range(1, 2):
        url = f'https://eda.ru/recepty?page={count}' 
        response = requests.get(url) 
            
        bs = BeautifulSoup(response.content.decode('utf-8'), 'html.parser') 
            
        tables = bs.find_all("div", attrs={'class':"emotion-1f6ych6"})
        
        for i in tables:
            card_url ="https://eda.ru/" +  i.find("a").get('href')
            yield card_url
        

def array():
    for card_url in get_url():
        response = requests.get(card_url)
        bs = BeautifulSoup(response.content.decode('utf-8'), 'html.parser') 
        one = bs.find_all('span', attrs= {'itemprop':"name"}) 
        for m in one: 
            name = m.text
        descr = bs.find('span', attrs={'class' : "emotion-aiknw3"})
        description = descr.text if descr else ""
        
        ingredients = bs.find_all('div', attrs={'class': 'emotion-1oyy8lz'})
        for i in ingredients:
            ingredient_name = i.find('span', attrs={'class': 'emotion-mdupit'}).text
            ingredient_count = i.find('span', attrs={'class': 'emotion-bsdd3p'}).text
            # yield ingredient_name, ingredient_count
        
        rechept = bs.find_all("div", attrs={"itemprop": "recipeInstructions"})
        for i in rechept:
            number = int(i.find("span", {"class": "emotion-1hreea5"}).text)
            text = i.find("span", {"itemprop": "text"}).text
            # yield number, text

        video = bs.find('meta', attrs={'itemprop' : "embedUrl"}).get('content')
        
        yield name, description, (ingredient_name, ingredient_count), (number, text), video 
        
        