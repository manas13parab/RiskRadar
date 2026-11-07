from flask import Flask

from backend.config import SECRET_KEY
from backend.db import init_db, seed_db
from backend.routes import register_routes

app = Flask(__name__)
app.secret_key = SECRET_KEY

init_db()
seed_db()

# All pages live in backend/routes/ (auth_routes, teacher_routes, student_routes)
register_routes(app)


if __name__ == "__main__":
    # Run with:  python app.py   (or: flask run)   ->  http://127.0.0.1:5000
    app.run(debug=True)
