# 🎬 Movie Recommendation System

This is a content-based movie recommendation system built using Python and Streamlit. It recommends similar movies based on your selection and excludes movies you’ve already watched.

## 💡 Features

- Recommends 5 similar movies using content-based filtering
- Excludes already watched movies
- Fetches movie posters and metadata using TMDb API
- Built using `pandas`, `scikit-learn`, and `Streamlit`

## 🗂️ Project Files

- `ui.py` – Main Streamlit web app
- `MR.ipynb` – Jupyter Notebook for processing and model creation
- `movie_data.pkl`, `similarity.pkl`, `details.pkl` – Precomputed data
- `tmdb_5000_credits.csv` – Dataset used for training
- `requirements.txt` – Required libraries

## ▶️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/movie-recommendation-system.git
   cd movie-recommendation-system
2. install dependencies:
   ```bash
   pip install -r requirements.txt
3. Set your TMDb API key (optional, used for fetching posters):
    ```bash
    export TMDB_API_KEY=your_api_key_here
4. Run the app:
   ```bash
   streamlit run ui.py
