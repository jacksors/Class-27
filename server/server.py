import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

def seed_db():
    conn = sqlite3.connect("movies.db")
    c = conn.cursor()
    # Clear existing movies table
    c.execute("DROP TABLE IF EXISTS movies")
    # Create a fresh movies table
    c.execute(""" 
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            duration INTEGER,
            director TEXT,
            description TEXT
        )
    """)
    # Sample data
    movies = [
        (
            "The Shawshank Redemption", 1994, "Drama", 142, "Frank Darabont",
            "Two imprisoned men bond over a number of years, finding solace and eventual redemption."
        ),
        (
            "The Godfather", 1972, "Crime", 175, "Francis Ford Coppola",
            "The aging patriarch of an organized crime dynasty transfers control to his reluctant son."
        ),
        (
            "The Dark Knight", 2008, "Action", 152, "Christopher Nolan",
            "Batman faces the Joker, who unleashes chaos on Gotham City."
        ),
        (
            "Forrest Gump", 1994, "Drama", 142, "Robert Zemeckis",
            "A simple man's extraordinary life intertwined with major historical events."
        ),
        (
            "Inception", 2010, "Sci-Fi", 148, "Christopher Nolan",
            "A thief invades dreams to plant an idea in a target's subconscious."
        )
    ]
    # Insert sample data
    c.executemany("""
        INSERT INTO movies (title, year, genre, duration, director, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, movies)
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title', '')
        year = request.form.get('year', '')
        genre = request.form.get('genre', '')
        duration = request.form.get('duration', '')
        director = request.form.get('director', '')
        description = request.form.get('description', '')

        if title:  # Minimal check: only insert if title is provided
            conn = sqlite3.connect("movies.db")
            c = conn.cursor()
            c.executescript(f"INSERT INTO movies (title, year, genre, duration, director, description)\
             VALUES\
              ('{title}', '{year}', '{genre}', '{duration}', '{director}', '{description}')")
            conn.commit()
            conn.close()


    # Fetch all movies to display
    conn = sqlite3.connect("movies.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM movies")
    movies = c.fetchall()
    conn.close()

    # Inline HTML template
    html = """
    <html>
    <head><title>Movie Catalog</title></head>
    <body>
        <h1>Movie Catalog</h1>
        <form method="POST">
            <p>Title: <input type="text" name="title"></p>
            <p>Year: <input type="number" name="year"></p>
            <p>Genre: <input type="text" name="genre"></p>
            <p>Duration: <input type="number" name="duration"></p>
            <p>Director: <input type="text" name="director"></p>
            <p>Description: <br><textarea name="description" rows="3" cols="40"></textarea></p>
            <p><button type="submit">Add Movie</button></p>
        </form>
        <ul>
        {% for movie in movies %}
            <li>
                <strong>{{ movie['title'] }} ({{ movie['year'] }})</strong><br>
                Genre: {{ movie['genre'] }}<br>
                Duration: {{ movie['duration'] }} min<br>
                Director: {{ movie['director'] }}<br>
                {{ movie['description'] }}
            </li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, movies=movies)

if __name__ == '__main__':
    # Seed the database on startup
    seed_db()
    # Run the Flask development server
    app.run(debug=True, host="0.0.0.0", port=8000)
