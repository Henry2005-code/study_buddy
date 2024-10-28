import io
import tempfile
from pypdf import PdfReader
from flask import current_app
import openai
import tiktoken

# Additional imports for new file types
from docx import Document
import pytesseract
from PIL import Image

def extract_text(file_stream, filename):
    try:
        filename = filename.lower()
        if filename.endswith('.pdf'):
            reader = PdfReader(file_stream)
            text = ''
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
        elif filename.endswith('.txt'):
            return file_stream.read().decode('utf-8')
        elif filename.endswith('.docx'):
            file_stream.seek(0)
            document = Document(io.BytesIO(file_stream.read()))
            text = '\n'.join([para.text for para in document.paragraphs])
            return text
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            file_stream.seek(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp_file:
                tmp_file.write(file_stream.read())
                tmp_file.flush()
                image = Image.open(tmp_file.name)
                text = pytesseract.image_to_string(image)
            return text
        else:
            # Handle unsupported file types
            return None
    except Exception as e:
        current_app.logger.exception('Error extracting text from file')
        raise None

def split_text_into_chunks(text, max_tokens=2000, encoding_name="gpt2"):
    # Use tiktoken to encode the text and split into chunks
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks

# utils.py

import openai
import json
from flask import current_app
from tiktoken import Encoding

def generate_flashcards(text, num_flashcards=5):
    openai.api_key = current_app.config['OPENAI_API_KEY']
    chunks = split_text_into_chunks(text, max_tokens=2000)
    all_flashcards = []

    for chunk in chunks:
        prompt = f"""
You are an expert educational assistant.

Create {num_flashcards} flashcards from the following text.

**Instructions:**
- Each flashcard should have a 'front' and a 'back'.
- Return the flashcards in JSON format as a list of dictionaries.
- Do not include any extra text; only output valid JSON.

**Text:**
{chunk}

**Output Format:**
[
  {{"front": "Question 1", "back": "Answer 1"}},
  {{"front": "Question 2", "back": "Answer 2"}}
]
"""
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            flashcards_text = response['choices'][0]['message']['content'].strip()
            flashcards = json.loads(flashcards_text)
            all_flashcards.extend(flashcards)
        except (openai.error.OpenAIError, json.JSONDecodeError) as e:
            current_app.logger.error(f"Error generating flashcards: {str(e)}")
            # Optionally, you can handle this error by skipping this chunk or returning an error message.
            continue

    return all_flashcards


def generate_quizzes(text, num_questions=5):
    openai.api_key = current_app.config['OPENAI_API_KEY']
    chunks = split_text_into_chunks(text, max_tokens=2000)
    all_quizzes = []

    for chunk in chunks:
        prompt = f"""
You are an expert quiz generator.

Create {num_questions} multiple-choice questions from the following text.

**Instructions:**
- Each question should have:
  - 'question': The question text.
  - 'options': A list of four options.
  - 'answer': The correct option.
- Return the quizzes in JSON format as a list of dictionaries.
- Do not include any extra text; only output valid JSON.

**Text:**
{chunk}

**Output Format:**
[
  {{
    "question": "Question 1",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option B"
  }},
  {{
    "question": "Question 2",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option C"
  }}
]
"""
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.7
            )
            quizzes_text = response['choices'][0]['message']['content'].strip()
            quizzes = json.loads(quizzes_text)
            all_quizzes.extend(quizzes)
        except (openai.error.OpenAIError, json.JSONDecodeError) as e:
            current_app.logger.error(f"Error generating quizzes: {str(e)}")
            # Optionally, handle the error
            continue

    return all_quizzes
