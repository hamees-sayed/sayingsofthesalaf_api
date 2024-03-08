import os
import ast
import unicodedata
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


# App Initialization
app = Flask(__name__)
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(current_dir, 'db.sqlite3')}"
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


# Database Models
class Narration(db.Model):
    __tablename__ = "narrations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    articles = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False)
    categories = db.Column(db.String, nullable=False)

    
# Utility functions
def decode_unicode(text):
    """Decode unicode text to ascii and remove special characters.
    Example: before: 'Al-Ḥasan Al-Baṣrī' | after: 'al-hasan-al-basri'"""
    return str(unicodedata.normalize('NFKD', text).encode('ascii', 'ignore'))[2:].replace("'", "").replace(".", "").replace(" ", "-").lower()

def get_names():
    """Get all narrators from the database."""
    narrations = Narration.query.all()
    narrators_list = set()
    for narration in narrations:
        for narrator in ast.literal_eval(narration.tags):
            narrators_list.add(narrator)
    return sorted(list(narrators_list))

def get_categories():
    """Get all categories from the database."""
    narrations = Narration.query.all()
    category_list = set()
    for narration in narrations:
        for category in ast.literal_eval(narration.categories):
            category_list.add(category)
    return sorted(list(category_list))


# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Not Found"}), 404

# Get every narration
@app.route('/')
def narrations():
    narrations = Narration.query.all()
    narrations_json = [{"id": narration.id, "articles": narration.articles, 
                        "categories": ast.literal_eval(narration.categories), "tags": ast.literal_eval(narration.tags)} for narration in narrations]
    return jsonify(narrations_json)

# Get a specific narration by id
@app.route('/<int:id>')
def athar(id):
    narration = Narration.query.get_or_404(id)
    narration_json = {"id": narration.id, "articles": narration.articles, 
                      "categories": ast.literal_eval(narration.categories), "tags": ast.literal_eval(narration.tags)}
    return jsonify(narration_json)

# Get all categories
@app.route('/category')
def categories():
    categories = get_categories()
    return categories

# Get a specific category by name
@app.route('/category/<string:category>')
def category(category):
    categories_list = get_categories()
    narrations = Narration.query.all()
    for cat in categories_list:
        if category == decode_unicode(cat):
            narrations_json = [{"id": narration.id,
                                "articles": narration.articles,
                                "categories": ast.literal_eval(narration.categories),
                                "tags": ast.literal_eval(narration.tags)}
                                for narration in narrations if cat in ast.literal_eval(narration.categories)]
            return jsonify(narrations_json)
        
    return jsonify({"error": "Not Found"}), 404

# Get all narrators
@app.route('/names')
def names():
    names = get_names()
    return names

# Get narratios by a specific narrator by name
@app.route('/names/<string:name>')
def salaf(name):
    name_list = get_names()
    narrations = Narration.query.all()
    for narrator in name_list:
        if name == decode_unicode(narrator):
            narrations_json = [{"id": narration.id,
                                "articles": narration.articles,
                                "categories": ast.literal_eval(narration.categories),
                                "tags": ast.literal_eval(narration.tags)}
                               for narration in narrations if narrator in ast.literal_eval(narration.tags)]
            return jsonify(narrations_json)
        
    return jsonify({"error": "Not Found"}), 404


    
# Run the app
if __name__ == "__main__":
    app.run()
