# models.py
from database import db  # Import db from database.py

class UserData(db.Model):
    __tablename__ = 'user_data'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

class GeneratedContent(db.Model):
    __tablename__ = 'generated_content'
    id = db.Column(db.Integer, primary_key=True)
    user_data_id = db.Column(db.Integer, db.ForeignKey('user_data.id'), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # 'flashcards' or 'quizzes'
    content = db.Column(db.Text, nullable=False)
