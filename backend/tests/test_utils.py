# tests/test_utils.py
import unittest
from unittest.mock import patch, mock_open, MagicMock
from io import BytesIO
from utils import extract_text, split_text_into_chunks, generate_flashcards, generate_quizzes
from flask import Flask, current_app
import openai

class TestUtils(unittest.TestCase):
    def setUp(self):
        # Set up a test Flask app context
        self.app = Flask(__name__)
        self.app.config['OPENAI_API_KEY'] = 'test-api-key'
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        # Pop the app context
        self.ctx.pop()

    def test_extract_text_pdf(self):
        # Mock the PDF reader
        with patch('utils.PdfReader') as mock_pdf_reader:
            mock_reader_instance = mock_pdf_reader.return_value
            mock_reader_instance.pages = [MagicMock()]
            mock_reader_instance.pages[0].extract_text.return_value = 'Sample PDF text.'

            file_stream = BytesIO(b'%PDF-1.4 sample content')
            filename = 'sample.pdf'

            text = extract_text(file_stream, filename)
            self.assertEqual(text, 'Sample PDF text.')

    def test_extract_text_txt(self):
        file_stream = BytesIO(b'Sample text file content.')
        filename = 'sample.txt'

        text = extract_text(file_stream, filename)
        self.assertEqual(text, 'Sample text file content.')

    def test_extract_text_docx(self):
        with patch('utils.Document') as mock_document:
            mock_document_instance = mock_document.return_value
            mock_document_instance.paragraphs = [MagicMock(text='Sample DOCX text.')]

            file_stream = BytesIO(b'DOCX file content')
            filename = 'sample.docx'

            text = extract_text(file_stream, filename)
            self.assertEqual(text, 'Sample DOCX text.')

    def test_extract_text_image(self):
        with patch('utils.Image.open') as mock_image_open, \
             patch('utils.pytesseract.image_to_string') as mock_ocr:
            mock_ocr.return_value = 'Sample OCR text.'

            file_stream = BytesIO(b'Image file content')
            filename = 'sample.png'

            text = extract_text(file_stream, filename)
            self.assertEqual(text, 'Sample OCR text.')

    def test_extract_text_unsupported(self):
        file_stream = BytesIO(b'Unsupported file content')
        filename = 'sample.xyz'

        text = extract_text(file_stream, filename)
        self.assertIsNone(text)

    def test_split_text_into_chunks(self):
        text = 'This is a sample text that will be split into chunks.'
        chunks = split_text_into_chunks(text, max_tokens=5, encoding_name='gpt2')
        self.assertIsInstance(chunks, list)
        self.assertTrue(len(chunks) > 0)

    @patch('utils.openai.ChatCompletion.create')
    def test_generate_flashcards(self, mock_openai_chat):
        mock_openai_chat.return_value = {
            'choices': [
                {'message': {'content': 'Flashcard content'}}
            ]
        }
        text = 'Sample text for flashcards.'
        flashcards = generate_flashcards(text, num_flashcards=2)
        self.assertIn('Flashcard content', flashcards)

    @patch('utils.openai.ChatCompletion.create')
    def test_generate_quizzes(self, mock_openai_chat):
        mock_openai_chat.return_value = {
            'choices': [
                {'message': {'content': 'Quiz content'}}
            ]
        }
        text = 'Sample text for quizzes.'
        quizzes = generate_quizzes(text, num_questions=2)
        self.assertIn('Quiz content', quizzes)

if __name__ == '__main__':
    unittest.main()
