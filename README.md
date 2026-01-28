# 🎬 Movie Recommendation System

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-360/)

A machine learning-powered movie recommendation system built with Streamlit that suggests movies based on user preferences and similarity metrics. The system uses K-Nearest Neighbors (KNN) algorithm with cosine similarity to find movies similar to your favorites or based on genre preferences.

<img src="https://github.com/Varsha-1605/Movie-Recommendation-System/blob/main/yt_thumb.jpg" alt="Movie Recommendation System">

## 🌟 Features

- **Content-Based Recommendations**: Get movie suggestions based on a movie you like
- **Genre-Based Recommendations**: Discover movies by selecting your favorite genres
- **Real-Time Movie Details**: Fetches live data from IMDb including:
  - Movie posters
  - Plot summaries
  - IMDb ratings
  - Director and cast information
- **Interactive UI**: Clean and responsive Streamlit interface
- **Cosine Similarity Algorithm**: Uses NearestNeighbors from scikit-learn for accurate recommendations
- **Large Dataset**: Recommendations based on 5000+ movies from IMDb

## 📊 Dataset

This project uses the [IMDB Movie 5000 Dataset](https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset) from Kaggle, which contains information about:
- Movie titles
- Genres
- Directors and cast
- IMDb ratings
- Plot keywords
- And more...

## 🛠️ Technology Stack

- **Python 3.11**
- **Streamlit** - Web application framework
- **Scikit-learn** - Machine learning (K-Nearest Neighbors algorithm)
- **Pandas & NumPy** - Data manipulation and analysis
- **BeautifulSoup4** - Web scraping for live IMDb data
- **Pillow** - Image processing
- **Requests** - HTTP library for fetching movie details

## 📁 Project Structure

```
Movie-Recommendation-System/
├── App.py                          # Main Streamlit application
├── Classifier.py                   # KNN classifier implementation
├── Movie_Data_Processing.ipynb     # Data preprocessing notebook
├── requirements.txt                # Python dependencies
├── Data/
│   ├── movie_data.json            # Processed movie features
│   └── movie_titles.json          # Movie titles and IMDb links
├── t1.png                         # Screenshot - Movie-based recommendation
├── t2.png                         # Screenshot - Genre-based recommendation
└── yt_thumb.jpg                   # Project thumbnail
```

## 🚀 Installation & Usage

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Varsha-1605/Movie-Recommendation-System.git
   cd Movie-Recommendation-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run App.py
   ```

4. **Access the app**
   - The application will automatically open in your default browser
   - If not, navigate to `http://localhost:8501`

## 💡 How It Works

### 1. **K-Nearest Neighbors Algorithm**
The system uses a custom KNN implementation (`Classifier.py`) with cosine similarity to find movies that are closest to:
- A selected movie (content-based filtering)
- User-selected genre preferences

### 2. **Feature Engineering**
Movies are represented as feature vectors based on:
- Genres
- Keywords
- Director
- Cast
- Other metadata

### 3. **Real-Time Data Fetching**
The app scrapes IMDb for the latest:
- Movie posters
- Ratings
- Plot summaries
- Cast information

## 📸 Screenshots

### Movie-Based Recommendation
Find similar movies based on a movie you already love.

<img src="https://github.com/Varsha-1605/Movie-Recommendation-System/blob/main/t1.png" alt="Movie based recommendations">

### Genre-Based Recommendation
Discover new movies by selecting your favorite genres.

<img src="https://github.com/Varsha-1605/Movie-Recommendation-System/blob/main/t2.png" alt="Genre based recommendations">

## 🔧 Data Processing

The `Movie_Data_Processing.ipynb` notebook contains:
- Data cleaning and preprocessing steps
- Feature extraction and encoding
- Generation of `movie_data.json` and `movie_titles.json`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Varsha**
- GitHub: [@Varsha-1605](https://github.com/Varsha-1605)

## 🙏 Acknowledgments

- Dataset from [Kaggle - IMDB 5000 Movie Dataset](https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset)
- IMDb for movie information
- Streamlit for the amazing web framework

---

⭐ If you found this project helpful, please give it a star!