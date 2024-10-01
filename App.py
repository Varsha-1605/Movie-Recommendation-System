import streamlit as st
from PIL import Image
import json
import requests
from bs4 import BeautifulSoup
import io
import PIL.Image
from urllib.request import urlopen
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
st.set_page_config(page_title="Enhanced Movie Recommender", layout="wide")
# Load data
@st.cache_data
def load_data():
    with open('./Data/movie_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('./Data/movie_titles.json', 'r', encoding='utf-8') as f:
        movie_titles = json.load(f)
    return data, movie_titles

data, movie_titles = load_data()

# Create a DataFrame for easier data manipulation
df = pd.DataFrame(data)
df['title'] = [title[0] for title in movie_titles]
df['imdb_link'] = [title[2] for title in movie_titles]

# Prepare feature matrix
feature_cols = df.columns[:-3]  # Exclude title, imdb_link, and imdb_score
X = df[feature_cols]

# Initialize NearestNeighbors model
nn_model = NearestNeighbors(n_neighbors=21, metric='cosine')
nn_model.fit(X)

def get_recommendations(query, n_recommendations=20):
    if isinstance(query, str):
        # If query is a movie title
        idx = df[df['title'] == query].index[0]
        distances, indices = nn_model.kneighbors(X.iloc[idx].values.reshape(1, -1))
    else:
        # If query is a feature vector
        distances, indices = nn_model.kneighbors(np.array(query).reshape(1, -1))
    
    return df.iloc[indices[0][1:n_recommendations+1]]

def fetch_movie_details(imdb_link):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(imdb_link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract movie details
        title = soup.find('h1')
        title = title.text.strip() if title else "Title not found"
        
        rating_elem = soup.find('span', class_='sc-bde20123-1') or soup.find('span', class_='sc-7ab21ed2-1')
        rating = rating_elem.text.strip() if rating_elem else "Rating not available"
        
        summary_elem = soup.find('span', class_='sc-466bb6c-2') or soup.find('span', attrs={"data-testid": "plot-xl"})
        summary = summary_elem.text.strip() if summary_elem else "Summary not available"
        
        # Extract poster URL
        poster_elem = soup.find('div', class_='ipc-media ipc-media--poster-27x40') or soup.find('div', class_='poster')
        poster_url = poster_elem.find('img')['src'] if poster_elem and poster_elem.find('img') else None
        
        return {
            'title': title,
            'rating': rating,
            'summary': summary,
            'poster_url': poster_url
        }
    except Exception as e:
        st.error(f"An error occurred while fetching movie details: {str(e)}")
        return {
            'title': "Error fetching details",
            'rating': "N/A",
            'summary': "Unable to fetch movie details. Please try again later.",
            'poster_url': None
        }

# Update the main function to handle potential errors
def main():
    st.title("Enhanced Movie Recommender System")
    st.markdown("Discover your next favorite movie!")

    # Sidebar for user input
    st.sidebar.header("Customize Your Recommendations")
    rec_type = st.sidebar.radio("Recommendation Type", ["Movie-based", "Genre-based"])

    if rec_type == "Movie-based":
        selected_movie = st.sidebar.selectbox("Select a movie", df['title'].tolist())
        recommendations = get_recommendations(selected_movie)
    else:
        genres = feature_cols[:-1]  # Exclude imdb_score
        selected_genres = st.sidebar.multiselect("Select genres", genres)
        imdb_score = st.sidebar.slider("Minimum IMDb Score", 1.0, 10.0, 7.0, 0.1)
        
        query = [1 if genre in selected_genres else 0 for genre in genres]
        query.append(imdb_score)
        recommendations = get_recommendations(query)

    # Display recommendations
    for _, movie in recommendations.iterrows():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            details = fetch_movie_details(movie['imdb_link'])
            if details['poster_url']:
                st.image(details['poster_url'], width=200)
            else:
                st.write("Poster not available")
        
        with col2:
            st.subheader(details['title'])
            st.write(f"IMDb Rating: {details['rating']}")
            st.write(details['summary'])
            st.write(f"[View on IMDb]({movie['imdb_link']})")

if __name__ == "__main__":
    main()
