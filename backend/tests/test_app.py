# tests/test_app.py
import unittest
from app import app, db
from flask import json
from io import BytesIO
from unittest.mock import patch

class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client and in-memory database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_upload_file_txt(self):
        data = {
            'document': (BytesIO(b'Sample text file content.'), 'sample.txt')
        }
        response = self.client.post('/upload', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertIn('user_data_id', json_data)

    def test_upload_file_pdf(self):
        with patch('utils.PdfReader') as mock_pdf_reader:
            mock_reader_instance = mock_pdf_reader.return_value
            mock_reader_instance.pages = [unittest.mock.MagicMock()]
            mock_reader_instance.pages[0].extract_text.return_value = 'Sample PDF text.'

            data = {
                'document': (BytesIO(b'%PDF-1.4 sample content'), 'sample.pdf')
            }
            response = self.client.post('/upload', content_type='multipart/form-data', data=data)
            self.assertEqual(response.status_code, 200)
            json_data = json.loads(response.data)
            self.assertIn('user_data_id', json_data)

    def test_upload_file_unsupported(self):
        data = {
            'document': (BytesIO(b'Unsupported content'), 'sample.xyz')
        }
        response = self.client.post('/upload', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertIn('error', json_data)

    @patch('app.generate_flashcards')
    def test_generate_content_flashcards(self, mock_generate_flashcards):
        mock_generate_flashcards.return_value = 'Generated flashcards.'
        # First, upload a file to get a user_data_id
        with self.client as c:
            data = {
                'document': (BytesIO(b'Sample text file content.'), 'sample.txt')
            }
            upload_response = c.post('/upload', content_type='multipart/form-data', data=data)
            json_data = json.loads(upload_response.data)
            user_data_id = json_data.get('user_data_id')

            # Now, generate content
            generate_data = {
                'user_data_id': user_data_id,
                'content_type': 'flashcards',
                'num_items': 5
            }
            response = c.post('/generate', json=generate_data)
            self.assertEqual(response.status_code, 200)
            json_response = json.loads(response.data)
            self.assertIn('generated_content', json_response)
            self.assertEqual(json_response['generated_content'], 'Generated flashcards.')

    @patch('app.generate_quizzes')
    def test_generate_content_quizzes(self, mock_generate_quizzes):
        mock_generate_quizzes.return_value = 'Generated quizzes.'
        # First, upload a file to get a user_data_id
        with self.client as c:
            data = {
                'document': (BytesIO(b'Sample text file content.'), 'sample.txt')
            }
            upload_response = c.post('/upload', content_type='multipart/form-data', data=data)
            json_data = json.loads(upload_response.data)
            user_data_id = json_data.get('user_data_id')

            # Now, generate content
            generate_data = {
                'user_data_id': user_data_id,
                'content_type': 'quizzes',
                'num_items': 5
            }
            response = c.post('/generate', json=generate_data)
            self.assertEqual(response.status_code, 200)
            json_response = json.loads(response.data)
            self.assertIn('generated_content', json_response)
            self.assertEqual(json_response['generated_content'], 'Generated quizzes.')

    def test_generate_content_invalid_user_data_id(self):
        generate_data = {
            'user_data_id': 999,  # Non-existent ID
            'content_type': 'flashcards',
            'num_items': 5
        }
        response = self.client.post('/generate', json=generate_data)
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.data)
        self.assertIn('error', json_response)

    def test_generate_content_invalid_content_type(self):
        # First, upload a file to get a user_data_id
        data = {
            'document': (BytesIO(b'Sample text file content.'), 'sample.txt')
        }
        upload_response = self.client.post('/upload', content_type='multipart/form-data', data=data)
        json_data = json.loads(upload_response.data)
        user_data_id = json_data.get('user_data_id')

        # Now, attempt to generate content with invalid content_type
        generate_data = {
            'user_data_id': user_data_id,
            'content_type': 'invalid_type',
            'num_items': 5
        }
        response = self.client.post('/generate', json=generate_data)
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.data)
        self.assertIn('error', json_response)

if __name__ == '__main__':
    unittest.main()
