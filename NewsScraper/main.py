import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from sqlalchemy import create_engine
import datetime 

now = datetime.datetime.now()

base_url = 'https://news.google.com/'
search_term = 'search?q=nri&hl=en-IN&gl=IN&ceid=IN%3Aen'

html_doc = requests.get(base_url+search_term)
soup = bs(html_doc.content, 'html.parser')

scrap_data = []

images_of_articles = soup.find_all('img', class_='tvs3Id QwxBBf')

articles = soup.find_all('div', class_='NiLAwe')
for ele in articles:
    if(ele.find('img', class_='tvs3Id QwxBBf')) != None: 
        scrap_data.append({
            'publisher': ele.find('div', class_='SVJrMe').a.text,
            'published': ele.find('time')['datetime'],
            'title': ele.h3.a.text,
            'description': ele.find('div', {'jsname': 'jVqMGc'}).text,
            'img_src': ele.find('img', class_='tvs3Id QwxBBf')['src'],
        })
    else:
        scrap_data.append({
            'publisher': ele.find('div', class_='SVJrMe').a.text,
            'published': ele.find('time')['datetime'],
            'title': ele.h3.a.text,
            'description': ele.find('div', {'jsname': 'jVqMGc'}).text,
            'img_src': '',
        })


conn = create_engine('postgresql://test:password@db:5432/test')
# conn = psycopg2.connect("user=test host=localhost password=test@123 dbname=test")
# c = conn.cursor()
df = pd.DataFrame(scrap_data)
df.to_sql('news_feed', conn, if_exists='replace', index = False)
#pd.read_sql_query("SELECT * FROM new_feed", conn)
print("\n--- Data updated successfully %s ---\n"%(now.strftime("%Y-%m-%d %H:%M:%S")))