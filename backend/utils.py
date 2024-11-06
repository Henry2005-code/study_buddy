# utils.py

import io
import tempfile
from pypdf import PdfReader
from flask import current_app
import openai
import tiktoken
import json
from math import ceil
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
        return None

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

def generate_flashcards(text, num_flashcards=5):
    openai.api_key = current_app.config['OPENAI_API_KEY']
    chunks = split_text_into_chunks(text, max_tokens=2000)
    all_flashcards = []
    total_chunks = len(chunks)
    items_per_chunk = ceil(num_flashcards / total_chunks) if total_chunks else num_flashcards

    for idx, chunk in enumerate(chunks):
        # Adjust items_per_chunk for the last chunk to avoid exceeding num_flashcards
        if idx == total_chunks - 1:
            items_to_generate = num_flashcards - len(all_flashcards)
            if items_to_generate <= 0:
                break
        else:
            items_to_generate = items_per_chunk

        prompt = f"""
You are an expert educational assistant.

Create {items_to_generate} flashcards from the following text.

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
                model='gpt-4',  # Corrected model name
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            flashcards_text = response['choices'][0]['message']['content'].strip()
            flashcards = json.loads(flashcards_text)
            all_flashcards.extend(flashcards)
            if len(all_flashcards) >= num_flashcards:
                break
        except (openai.error.OpenAIError, json.JSONDecodeError) as e:
            current_app.logger.error(f"Error generating flashcards: {str(e)}")
            continue

    # Trim the list to the exact number of requested flashcards
    return all_flashcards[:num_flashcards]

def generate_quizzes(text, num_questions=5):
    openai.api_key = current_app.config['OPENAI_API_KEY']
    chunks = split_text_into_chunks(text, max_tokens=2000)
    all_quizzes = []
    total_chunks = len(chunks)
    items_per_chunk = ceil(num_questions / total_chunks) if total_chunks else num_questions

    for idx, chunk in enumerate(chunks):
        # Adjust items_per_chunk for the last chunk to avoid exceeding num_questions
        if idx == total_chunks - 1:
            items_to_generate = num_questions - len(all_quizzes)
            if items_to_generate <= 0:
                break
        else:
            items_to_generate = items_per_chunk

        prompt = f"""
You are an expert quiz generator.

Create {items_to_generate} multiple-choice questions from the following text.

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
                model='gpt-4',  # Corrected model name
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.7
            )
            quizzes_text = response['choices'][0]['message']['content'].strip()
            quizzes = json.loads(quizzes_text)
            all_quizzes.extend(quizzes)
            if len(all_quizzes) >= num_questions:
                break
        except (openai.error.OpenAIError, json.JSONDecodeError) as e:
            current_app.logger.error(f"Error generating quizzes: {str(e)}")
            continue

    # Trim the list to the exact number of requested quizzes
    return all_quizzes[:num_questions]
