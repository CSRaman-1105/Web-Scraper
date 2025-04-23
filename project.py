import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def get_webpage_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'} 
    response = requests.get(url, headers=headers)
    response.raise_for_status() 
    return response.content 

def parse_html(content):
    return BeautifulSoup(content, 'html.parser')

def extract_movie_data(movie, index):
    rank = index + 1
    name = movie.get("name", "N/A") 
    description = movie.get("description", "N/A")  
    rating_value = movie.get("aggregateRating", {}).get("ratingValue", "N/A")  
    rating_count = movie.get("aggregateRating", {}).get("ratingCount", "N/A") 
    content_rating = movie.get("contentRating", "N/A")  
    genre = movie.get("genre", "N/A") 
    duration = movie.get("duration", "N/A").replace("PT", "").lower()  

    return rank, name, description, rating_value, rating_count, content_rating, genre, duration



def scrape_imdb_top_movies(url):
    content = get_webpage_content(url)
    soup = parse_html(content)

    # Locate the JSON script tag
    script_tag = soup.find('script', type="application/ld+json")
    if not script_tag:
        raise ValueError("Could not find the JSON data in the script tag")

    json_data = script_tag.string
    data = json.loads(json_data)

    movies = data.get("itemListElement", [])
    if not movies:
        raise ValueError("No movies found in the JSON data")

    movie_data = []
    for index, movie in enumerate(movies):
        movie_data.append(extract_movie_data(movie.get("item", {}), index))

    return movie_data


def save_as_csv(movie_data):
    df = pd.DataFrame(movie_data, columns=[
        'Rank', 'Name', 'Description', 'IMDb Rating', 'Votes', 'Content Rating', 'Genre', 'Duration'
    ])
    df.to_csv("IMDB_Top_250_Movies.csv", index=False)
    print("Data successfully saved to IMDB_Top_250_Movies.csv")


def save_as_json(movie_data):
    df = pd.DataFrame(movie_data, columns=[
        'Rank', 'Name', 'Description', 'IMDb Rating', 'Votes', 'Content Rating', 'Genre', 'Duration'
    ])
    df.to_json("IMDB_Top_250_Movies.json", orient="records", indent=4, force_ascii=False)
    print("Data successfully saved to IMDB_Top_250_Movies.json")


def main():
    url = "https://www.imdb.com/chart/top"
    movie_data = scrape_imdb_top_movies(url)

    if movie_data:
        for movie in movie_data:
            print("Rank: {}, Name: {}, Description: {}, IMDb Rating: {}, Votes: {}, Content Rating: {}, Genre: {}, Duration: {}"
                  .format(*movie))
        save_as_csv(movie_data) 
        save_as_json(movie_data)  
    else:
        print("No movie data found.")



if __name__ == "__main__":
    main()