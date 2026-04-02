# 🎬 CineMatch: Movie Recommendation & Discovery System

A powerful, full-stack Django-based movie discovery platform that leverages the **TMDB (The Movie Database)** API to provide a comprehensive and interactive cinematic experience. 

CineMatch features a deep database of Bollywood, South Indian, and International cinema, complete with automated data synchronization, user reviews with sentiment analysis, and a modern, responsive user interface.

---

## 🌟 Key Features

### 🚀 Data & Integration
- **TMDB Smart Sync**: Automated management commands to fetch and update movies, TV shows, and artist (cast/crew) metadata directly from TMDB.
- **Deep Metadata**: Comprehensive tracking of directors, main actors, music directors, and even specific roles like villains and comedians.
- **Genre Taxonomy**: Full support for movie and TV show genres with distinct landing pages for each.

### 🎭 User Experience
- **AI-Powered Discovery**: Integrated facial recognition and emotion detection (using MTCNN and RetinaFace) to suggest movies based on the user's current mood.
- **Dynamic Categorization**: Dedicated sections for Bollywood hits, South Indian blockbusters, and Top Rated global cinema.
- **Intelligent Search**: Real-time search functionality covering movie titles and cast/crew names.
- **Sentiment-Aware Reviews**: User rating and review system that automatically calculates review sentiment (Positive/Negative/Neutral) using Natural Language Processing (NLP) via `TextBlob`.
- **Responsive Design**: A sleek, card-based UI that works seamlessly across desktops, tablets, and mobile devices.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Django 4.2+
- **Database**: PostgreSQL (with Full-Text Search integration)
- **AI & Computer Vision**: 
  - **TensorFlow & Keras**: Deep learning engine.
  - **MTCNN & RetinaFace**: High-accuracy face detection.
  - **OpenCV**: Real-time image processing.
- **Natural Language Processing**: TextBlob (Sentiment Analysis).
- **External API**: TMDB (v3)
- **Storage & Media**: Cloudinary (Media hosting) & WhiteNoise (Static files)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System), JavaScript

---

## 🚦 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL
- TMDB API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jas2005-ct/movie-recommendation.git
   cd movie-recommendation
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory based on `.env.example`:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   TMDB_API_KEY=your_tmdb_api_key
   DATABASE_URL=postgresql://user:password@localhost:5432/movies
   ```

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Initialize Data:**
   Use the custom sync scripts to populate your local database:
   ```bash
   # Sync movies from TMDB
   python manage.py sync_movies
   
   # Sync artist/crew metadata
   python manage.py sync_artists
   ```

7. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 📁 Project Structure

```text
movie_recommondation/
├── movie/               # Core application logic
│   ├── management/      # Custom sync commands (sync_movies, sync_artists)
│   ├── templatetags/    # Custom template filters
│   ├── models.py        # Database schema for Movies, Persons, Reviews, etc.
│   ├── views.py         # Template-based discovery and search views
│   └── urls.py          # App-specific routing
├── movies/              # Main project configuration (settings, asgi, wsgi)
├── static/              # CSS, JS, and global assets
├── template/            # HTML templates
├── .env.example         # Environment template
└── manage.py            # Django entry point
```

---

## 📝 Custom Management Commands

- `python manage.py sync_movies`: Fetches popular and trending movies across various categories (Bollywood, South, etc.) and saves them to the local PostgreSQL database.
- `python manage.py sync_artists`: Enriches the database by fetching detailed cast and crew information for existing movies.
- `python manage.py get_tmdb`: Utility for manual TMDB API interaction.

---

## 🌐 Deployment

This project is configured for easy deployment on platforms like **Render** or **Heroku** using the included `Procfile` and `runtime.txt`. It utilizes `dj-database-url` for easy database configuration and `cloudinary` for external media storage.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
