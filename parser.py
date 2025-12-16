import requests
from bs4 import BeautifulSoup
import time 
import pandas as pd 

def ratings(type_ratings): 
    data = []
    page_number = 1 
    
    while True: 
        URL = f'https://www.kinoafisha.info/rating/{type_ratings}/page-{page_number}/'  
        print(f"Обрабатываю страницу {page_number}: {URL}")
        
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'lxml') 
        entries = soup.find_all('div', class_='movieItem_info') 
        
        if len(entries) == 0:  
            print(f"Страница {page_number} не содержит данных. Завершаю сбор.")
            break 
        
        for entry in entries:
            film_name = entry.find('a', class_="movieItem_title").text  
            movieItem_details = entry.find('div', class_="movieItem_details")
            movieItem_genres = movieItem_details.find("span", class_="movieItem_genres").text 
            movieItem_year = movieItem_details.find("span", class_="movieItem_year").text  
            movieItem_actions = entry.find("div", class_="movieItem_actions") 
            
            if type_ratings in ["movies", "boxoffice"]: 
                rating_stars = movieItem_actions.find("div", class_='rating_stars')
                rating_val = rating_stars.find("span", class_='rating_val')
                classes = rating_val.get('style', [])
                rating = classes.split(':')[1].split(';')[0]  
                data.append({
                    "film_name": film_name, 
                    "film_gender": movieItem_genres, 
                    "year_country": movieItem_year,
                    "ratings_film": rating
                }) 
            else: 
                like_yes = entry.find("div", class_="like_item like_item-yes")
                like_num_yes = like_yes.find("span", class_="like_num").text 
                like_no = entry.find("div", class_="like_item like_item-no")
                like_num_no = like_no.find("span", class_="like_num").text 
                data.append({
                    "film_name": film_name, 
                    "film_gender": movieItem_genres, 
                    "year_country": movieItem_year, 
                    "yes": like_num_yes, 
                    "no": like_num_no
                }) 
        
        print(f"Обработано {len(entries)} фильмов на странице {page_number}")
        page_number += 1  
        time.sleep(2)
    
    print(f"Всего собрано {len(data)} записей")
    return data 


check_type = ratings(input("Введите тип рейтинга (movies/boxoffice/releases): ")) 

user_rates = check_type
df = pd.DataFrame(user_rates)

df.to_excel('C:/Users/Pavel/Desktop/folder/user_rates.xlsx', index=False)
