import os
import ast
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


# Get every narration
@app.route('/')
def narrations():
    narrations = Narration.query.all()
    narrations_json = [{"id": narration.id, "articles": narration.articles, 
                        "categories": ast.literal_eval(narration.categories), "tags": ast.literal_eval(narration.tags)} for narration in narrations]
    return jsonify(narrations_json)

# Get a specific narration
@app.route('/<int:id>')
def athar(id):
    narration = Narration.query.get_or_404(id)
    narration_json = {"id": narration.id, "articles": narration.articles, 
                      "categories": ast.literal_eval(narration.categories), "tags": ast.literal_eval(narration.tags)}
    return jsonify(narration_json)

# Get all categories
# @app.route('/topics')
    
if __name__ == "__main__":
    app.run(debug=True)