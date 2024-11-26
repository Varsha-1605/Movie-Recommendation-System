import streamlit as st
from PIL import Image
import json
from Classifier import KNearestNeighbours
from bs4 import BeautifulSoup
import requests, io
import PIL.Image
from urllib.request import urlopen


st.set_page_config(
    page_title="Movie Recommender System",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Enhanced Modern UI with Animations
st.markdown("""
<style>
    /* Modern Color Palette and Variables */
    :root {
        --primary-color: #6366F1;
        --primary-hover: #4F46E5;
        --background-dark: #0F172A;
        --card-bg: #1E293B;
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --accent-color: #22D3EE;
        --error-color: #EF4444;
        --success-color: #10B981;
        --warning-color: #F59E0B;
    }

    /* Base Styles */
    .stApp {
        background: linear-gradient(135deg, var(--background-dark) 0%, #1E1B4B 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Glass Morphism Effect */
    .glass-container {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    /* Modern Title Animation */
    .title {
        background: linear-gradient(120deg, var(--primary-color), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin: 2rem 0;
        animation: fadeInScale 1s ease-out;
    }

    @keyframes fadeInScale {
        0% {
            opacity: 0;
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }

    /* Subtitle with Gradient */
    .subtitle {
        color: var(--text-secondary);
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        animation: fadeIn 1s ease-out;
    }

    /* Enhanced Movie Cards */
    .movie-card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        background: linear-gradient(90deg, var(--primary-color) 0%, transparent 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }

    .movie-card:hover::before {
        opacity: 0.1;
    }

    /* Movie Content Layout */
    .movie-content {
        display: grid;
        grid-template-columns: auto 1fr;
        gap: 2rem;
        position: relative;
        z-index: 1;
    }

    /* Animated Movie Title */
    .movie-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(120deg, var(--text-primary), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        transition: all 0.3s ease;
    }

    .movie-title:hover {
        transform: translateX(10px);
    }

    /* Enhanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
    }

    /* Modern Select Boxes */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--card-bg);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: var(--text-primary);
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover {
        border-color: var(--primary-color);
    }

    /* Slider Styling */
    .stSlider > div > div > div {
        background: var(--primary-color);
    }

    .stSlider > div > div > div > div {
        background: var(--accent-color);
        box-shadow: 0 0 10px rgba(34, 211, 238, 0.5);
    }

    /* Rating Display */
    .rating {
        display: inline-flex;
        align-items: center;
        background: rgba(99, 102, 241, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: var(--accent-color);
        font-weight: 600;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .rating:hover {
        background: rgba(99, 102, 241, 0.2);
        transform: scale(1.05);
    }

    /* Movie Info Sections */
    .movie-info {
        color: var(--text-secondary);
        line-height: 1.8;
        margin: 0.75rem 0;
        padding-left: 1rem;
        border-left: 3px solid var(--primary-color);
        transition: all 0.3s ease;
    }

    .movie-info:hover {
        border-left-color: var(--accent-color);
        padding-left: 1.5rem;
    }

    /* Loading Animation */
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }

    .loading {
        background: linear-gradient(90deg, var(--card-bg) 0%, rgba(99, 102, 241, 0.1) 50%, var(--card-bg) 100%);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--background-dark);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-hover);
    }

    /* Error and Success Messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
        border: 1px solid var(--success-color);
        border-radius: 12px;
        color: #34D399;
        padding: 1rem;
        animation: slideIn 0.5s ease-out;
    }

    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05));
        border: 1px solid var(--warning-color);
        border-radius: 12px;
        color: #FBBF24;
        padding: 1rem;
        animation: slideIn 0.5s ease-out;
    }

    @keyframes slideIn {
        from {
            transform: translateX(-10px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
</style>
""", unsafe_allow_html=True)

# Define headers for requests
hdr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

def movie_poster_fetcher(imdb_link):
    try:
        url_data = requests.get(imdb_link, headers=hdr).text
        s_data = BeautifulSoup(url_data, 'html.parser')
        
        imdb_dp = s_data.find("meta", property="og:image")
        if not imdb_dp:
            imdb_dp = s_data.find("meta", property="og:image:url")
        if not imdb_dp:
            st.warning("Movie poster not available")
            return
            
        movie_poster_link = imdb_dp.attrs['content']
        u = urlopen(movie_poster_link)
        raw_data = u.read()
        image = PIL.Image.open(io.BytesIO(raw_data))
        image = image.resize((158, 301))
        
        st.image(image, use_column_width=False)
    except Exception as e:
        st.warning(f"Could not fetch movie poster: {str(e)}")

def get_movie_info(imdb_link):
    try:
        url_data = requests.get(imdb_link, headers=hdr).text
        s_data = BeautifulSoup(url_data, 'html.parser')
        
        imdb_content = s_data.find("meta", property="og:description")
        if not imdb_content:
            return "Director: Not available", "Cast: Not available", "Story: Not available", "Rating count: Not available"
            
        movie_descr = imdb_content.attrs['content']
        movie_descr = str(movie_descr).split('.')
        
        if len(movie_descr) >= 3:
            movie_director = movie_descr[0]
            movie_cast = str(movie_descr[1]).replace('With', 'Cast: ').strip()
            movie_story = 'Story: ' + str(movie_descr[2]).strip() + '.'
        else:
            movie_director = "Director: Not available"
            movie_cast = "Cast: Not available"
            movie_story = "Story: " + " ".join(movie_descr).strip()
        
        rating_elem = s_data.find(["span", "div"], class_=lambda x: x and "rating" in x.lower())
        if rating_elem:
            movie_rating = 'Total Rating count: ' + str(rating_elem.text)
        else:
            movie_rating = 'Total Rating count: Not available'
            
        return movie_director, movie_cast, movie_story, movie_rating
    except Exception as e:
        return f"Error: {str(e)}", "Cast: Not available", "Story: Not available", "Rating count: Not available"

def KNN_Movie_Recommender(test_point, k):
    try:
        target = [0 for item in movie_titles]
        model = KNearestNeighbours(data, target, test_point, k=k)
        model.fit()
        table = []
        for i in model.indices:
            table.append([movie_titles[i][0], movie_titles[i][2], data[i][-1]])
        return table
    except Exception as e:
        st.error(f"Error in recommendation algorithm: {str(e)}")
        return []

def load_data():
    try:
        with open('./Data/movie_data.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
        with open('./Data/movie_titles.json', 'r+', encoding='utf-8') as f:
            movie_titles = json.load(f)
        return data, movie_titles
    except Exception as e:
        st.error(f"Error loading data files: {str(e)}")
        return None, None




def run():

    # Load data
    global data, movie_titles
    data, movie_titles = load_data()
    if not data or not movie_titles:
        return

    # Center-align the logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            img1 = Image.open('./meta/logo.jpg')
            img1 = img1.resize((200, 200), Image.Resampling.LANCZOS)
            st.image(img1, use_column_width=False, width=180)
        except Exception as e:
            st.warning("Could not load logo image")

    st.markdown('<h1 class="title">Movie Recommender System</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Based on IMDB 5000 Movie Dataset</div>', unsafe_allow_html=True)

    with st.container():
        genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
                'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
                'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
        movies = [title[0] for title in movie_titles]
        category = ['--Select--', 'Movie based', 'Genre based']
        
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        cat_op = st.selectbox('Select Recommendation Type', category)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if cat_op == category[0]:
            st.warning('Please select Recommendation Type!')
        
        elif cat_op == category[1]:
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            select_movie = st.selectbox('Select movie: (Recommendation will be based on this selection)',
                                    ['--Select--'] + movies)
            
            if select_movie != '--Select--':
                no_of_reco = st.slider('Number of movies you want Recommended:', min_value=5, max_value=20, step=1)
                genres = data[movies.index(select_movie)]
                test_points = genres
                
                table = KNN_Movie_Recommender(test_points, no_of_reco + 1)
                if table:
                    table.pop(0)
                    dec = st.radio("Want to fetch movie posters?", ('Yes', 'No'), key='movie_based_posters')
                    st.markdown('<p class="info-text">* Fetching movie posters will take some time</p>', unsafe_allow_html=True)
                    st.success('Here are some movies you might like:')
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    for movie, link, ratings in table:
                        st.markdown(f'''
                            <div class="movie-card">
                                <div class="movie-title">
                                    <a href="{link}" target="_blank">{movie}</a>
                                </div>
                                <div class="movie-content">
                                    <div class="movie-poster">
                            ''', unsafe_allow_html=True)
                        
                        if dec == 'Yes':
                            movie_poster_fetcher(link)
                        
                        director, cast, story, total_rat = get_movie_info(link)
                        
                        st.markdown(f'''
                                    </div>
                                    <div class="movie-details">
                                        <div class="movie-info">{story}</div>
                                        <div class="movie-info">{total_rat}</div>
                                        <div class="rating">IMDB Rating: {ratings}⭐</div>
                                    </div>
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
            else:
                st.warning('Please select a movie!')
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif cat_op == category[2]:
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            sel_gen = st.multiselect('Select Genres:', genres)
            
            if sel_gen:
                imdb_score = st.slider('Choose minimum IMDB score:', 1.0, 10.0, 8.0, 0.1)
                no_of_reco = st.number_input('Number of movies:', min_value=5, max_value=20, step=1, value=10)
                
                dec = st.radio("Want to fetch movie posters?", ('Yes', 'No'), key='genre_based_posters')


                test_point = [1 if genre in sel_gen else 0 for genre in genres]
                test_point.append(imdb_score)
                
                table = KNN_Movie_Recommender(test_point, no_of_reco)
                if table:
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)
                    for movie, link, ratings in table:
                        st.markdown(f'''
                            <div class="movie-card">
                                <div class="movie-poster">
                        ''', unsafe_allow_html=True)
                        
                        if dec == 'Yes':
                            movie_poster_fetcher(link)
                        
                        director, cast, story, total_rat = get_movie_info(link)
                        
                        st.markdown(f'''
                                </div>
                                <div class="movie-details">
                                    <a href="{link}" target="_blank" class="movie-title">{movie}</a>
                                    <div class="movie-info">{story}</div>
                                    <div class="movie-info">{total_rat}</div>
                                    <div class="rating">⭐ IMDB Rating: {ratings}</div>
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning('Please select at least one genre!')
                st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    run()