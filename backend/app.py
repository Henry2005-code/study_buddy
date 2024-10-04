# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from config import Config
from utils import extract_text, generate_flashcards, generate_quizzes
from database import db  # Import db from database.py

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)  # Initialize db with the Flask app

# Import models after initializing db
from models import UserData, GeneratedContent

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'document' not in request.files:
            app.logger.error('No file part in the request')
            return jsonify({'error': 'No file part'}), 400
        file = request.files['document']
        if file.filename == '':
            app.logger.error('No file selected for uploading')
            return jsonify({'error': 'No selected file'}), 400
        content = extract_text(file.stream, file.filename)
        if content is None or content.strip() == '':
            app.logger.error('No content extracted from the file')
            return jsonify({'error': 'No content extracted from the file'}), 400
        user_data = UserData(filename=file.filename, content=content)
        db.session.add(user_data)
        db.session.commit()
        app.logger.info(f'File {file.filename} uploaded successfully with ID {user_data.id}')
        return jsonify({'message': 'File uploaded successfully', 'user_data_id': user_data.id}), 200
    except Exception as e:
        app.logger.exception('An error occurred during file upload')
        return jsonify({'error': 'An internal error occurred'}), 500

@app.route('/api/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        user_data_id = data.get('user_data_id')
        content_type = data.get('content_type')
        num_items = data.get('num_items', 5)

        user_data = UserData.query.get(user_data_id)
        if not user_data:
            return jsonify({'error': 'User data not found'}), 404

        if content_type == 'flashcards':
            generated_text = generate_flashcards(user_data.content, num_items)
        elif content_type == 'quizzes':
            generated_text = generate_quizzes(user_data.content, num_items)
        else:
            return jsonify({'error': 'Invalid content type'}), 400

        generated_content = GeneratedContent(
            user_data_id=user_data.id,
            content_type=content_type,
            content=generated_text
        )
        db.session.add(generated_content)
        db.session.commit()

        return jsonify({'generated_content': generated_text}), 200
    except Exception as e:
        app.logger.exception('An error occurred during content generation')
        return jsonify({'error': str(e)}), 500


@app.route('/api/test', methods=['GET'])
def api_test():
    return jsonify({'message': 'Backend API is working'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
