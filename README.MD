
# AI-Driven Learning Tool Backend

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Initialization](#database-initialization)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Upload File](#upload-file)
  - [Generate Content](#generate-content)
- [Handling Large Documents](#handling-large-documents)
- [Error Handling](#error-handling)
- [Testing the Backend](#testing-the-backend)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Next Steps](#next-steps)
- [License](#license)

---

## Overview

This project aims to develop an AI-driven learning tool that provides students with customized study aids, such as quizzes and flashcards, based on the content extracted from uploaded documents (e.g., PDFs, text files, images). The backend is built using Python and Flask, integrating with the OpenAI API to leverage natural language processing (NLP) for content analysis and study material generation.

## Features

- **File Upload:** Supports uploading of PDF and text files.
- **Automatic Study Material Generation:** Generates flashcards and quizzes based on the uploaded content.
- **Handling Large Documents:** Implements text chunking to manage large documents efficiently.
- **User Data Management:** Stores uploaded files and generated content in a SQLite database.
- **API Integration:** Utilizes the OpenAI API for NLP tasks.
- **Robust Error Handling:** Provides meaningful error messages and handles exceptions gracefully.

## Technologies Used

- **Backend:** Python, Flask
- **Database:** SQLite
- **NLP:** OpenAI API (`gpt-3.5-turbo` model)
- **Libraries:** Flask-RESTful, Flask-CORS, SQLAlchemy, PyPDF2, python-dotenv
- **Text Extraction**: PyPDF2/pypdf, python-docx, pytesseract, Pillow

## Setup Instructions

### Prerequisites

- **Python:** Version 3.7 or higher
- **pip:** Python package installer
- **Git:** For version control (optional)
- **OpenAI API Key:** Required for content generation

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/studybuddy.git
   cd backend
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - **On macOS and Linux:**

     ```bash
     source venv/bin/activate
     ```

   - **On Windows:**

     ```bash
     venv\Scripts\activate
     ```

3. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the project root directory to store environment variables securely.

```bash
touch .env
```

Add the following lines to the `.env` file:

```dotenv
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
MAX_CONTENT_LENGTH=10485760  # 10 MB limit
```

- **`SECRET_KEY`**: A secret key for Flask sessions and security.
- **`OPENAI_API_KEY`**: Your OpenAI API key for accessing the NLP services.
- **`MAX_CONTENT_LENGTH`**: (Optional) Maximum allowed payload to prevent large file uploads (default is set to 10 MB).

### Database Initialization

Initialize the SQLite database by running the Flask application. This will create the necessary tables.

```bash
python app.py
```

You should see output indicating that the Flask server is running. Once the server is running, you can stop it by pressing `Ctrl+C`. The `database.db` file should now exist in your project directory.

## Running the Application

Start the Flask backend server with the following command:

```bash
python app.py
```

The server will start and listen on `http://127.0.0.1:5000/`.

**Note:** Ensure that the virtual environment is activated before running the server.

## API Endpoints

### Upload File

- **URL:** `/upload`
- **Method:** `POST`
- **Description:** Uploads a document (PDF or text file) and extracts its content for study material generation.
- **Form Data:**
  - `document`: The file to be uploaded.
- **Response:**
  - **Success (200):**
    ```json
    {
      "message": "File uploaded successfully",
      "user_data_id": 1
    }
    ```
  - **Error (400 or 500):**
    ```json
    {
      "error": "Error message detailing what went wrong"
    }
    ```

### Generate Content

- **URL:** `/generate`
- **Method:** `POST`
- **Description:** Generates flashcards or quizzes based on the uploaded document's content.
- **JSON Body:**
  - `user_data_id` (integer, required): The ID of the uploaded content.
  - `content_type` (string, required): Type of content to generate (`"flashcards"` or `"quizzes"`).
  - `num_items` (integer, optional): Number of items to generate (default is 5).
- **Response:**
  - **Success (200):**
    ```json
    {
      "generated_content": "Generated flashcards or quizzes as a string."
    }
    ```
  - **Error (400 or 500):**
    ```json
    {
      "error": "Error message detailing what went wrong"
    }
    ```

## Handling Large Documents

To effectively manage large documents and ensure smooth operation within the OpenAI API's token limitations, the backend implements **text chunking**. Here's how it works:

1. **Text Extraction:** When a document is uploaded, its text content is extracted using `PyPDF2` for PDFs or standard text reading for text files.

2. **Chunking Mechanism:**
   - **Purpose:** Splits the extracted text into smaller chunks that fit within the OpenAI API's token limits (e.g., 2000 tokens per chunk).
   - **Implementation:** The `split_text_into_chunks` function divides the text into manageable segments.
   - **Processing:** Each chunk is processed individually to generate flashcards or quizzes. The results are then aggregated to form the final output.

3. **Summarization (Optional):**
   - For extremely large texts, the backend can optionally summarize content before chunking to reduce the amount of text being processed.

### **Advantages of Chunking**

- **Prevents Token Overflows:** Ensures that API requests do not exceed the maximum token limit.
- **Improves Performance:** Processes smaller text segments more efficiently.
- **Enhances Reliability:** Reduces the likelihood of errors during content generation.

### **Example Usage**

When generating flashcards:

```python
generated_flashcards = generate_flashcards(extracted_text, num_flashcards=10)
```

If `extracted_text` is too long, it will be split into chunks, each processed separately, and the results will be combined.

## Error Handling

The application includes robust error handling to manage various failure scenarios:

- **File Upload Errors:**
  - No file part in the request.
  - No file selected.
  - Unsupported file type.
  - File size exceeds the configured limit.

- **Processing Errors:**
  - Errors during text extraction.
  - OpenAI API request failures.
  - Database commit issues.

- **General Exceptions:**
  - Any unexpected errors are caught and returned as JSON responses with appropriate HTTP status codes.

**Example Error Response:**

```json
{
  "error": "Detailed error message explaining what went wrong."
}
```

## Testing the Backend

You can test the backend API using tools like **Postman**, **cURL**, or any other HTTP client.

### **1. Upload a File**

**Using cURL:**

```bash
curl -X POST -F "document=@/Users/henryfowobaje/Downloads/musictest.pdf" http://127.0.0.1:5000/upload
```

**Expected Response:**

```json
{
  "message": "File uploaded successfully",
  "user_data_id": 1
}
```

### **2. Generate Flashcards**

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "user_data_id": 1,
  "content_type": "flashcards",
  "num_items": 5
}' http://127.0.0.1:5000/generate
```

**Expected Response:**

```json
{
  "generated_content": "Generated flashcards content..."
}
```

### **3. Generate Quizzes**

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "user_data_id": 1,
  "content_type": "quizzes",
  "num_items": 5
}' http://127.0.0.1:5000/generate
```

**Expected Response:**

```json
{
  "generated_content": "Generated quizzes content..."
}
```

## Troubleshooting

If you're encountering issues, follow these steps to diagnose and resolve them:

### **1. Verify Server Status**

- **Ensure Flask Server is Running:**
  - Check the terminal where `app.py` is running for any error messages.
  - Restart the server if necessary:

    ```bash
    python app.py
    ```

### **2. Check File Path and Permissions**

- **Ensure File Exists:**

  ```bash
  ls -l /Users/henryfowobaje/Downloads/musictest.pdf
  ```

- **Check Read Permissions:**

  ```bash
  chmod +r /Users/henryfowobaje/Downloads/musictest.pdf
  ```

### **3. Review Server Logs**

- **Monitor Terminal Output:**
  - Look for any error messages or stack traces when making API requests.

### **4. Use Verbose cURL Output**

- **Run cURL with Verbosity:**

  ```bash
  curl -v -X POST -F "document=@/Users/henryfowobaje/Downloads/musictest.pdf" http://127.0.0.1:5000/upload
  ```

- **Analyze Output:**
  - Check for HTTP status codes and error messages.

### **5. Validate Environment Variables**

- **Ensure `.env` is Correctly Configured:**
  - Check that `SECRET_KEY` and `OPENAI_API_KEY` are set.
  - Verify that `.env` is in the project root and properly formatted.

### **6. Confirm Database Initialization**

- **Check for `database.db`:**
  - Ensure the SQLite database file exists in the project directory.
  - If not, run the server to initialize it.

### **7. Handle Large Files Appropriately**

- **Respect `MAX_CONTENT_LENGTH`:**
  - Ensure that uploaded files do not exceed the maximum allowed size.
  - If necessary, adjust `MAX_CONTENT_LENGTH` in `.env` and `config.py`.

### **8. Test with Different Files**

- **Upload a Smaller or Different File:**

  ```bash
  curl -X POST -F "document=@/path/to/smallfile.txt" http://127.0.0.1:5000/upload
  ```

### **9. Use Postman for Detailed Testing**

- **Set Up Request in Postman:**
  - **Method:** POST
  - **URL:** `http://127.0.0.1:5000/upload`
  - **Body:** Form-data
    - Key: `document`
    - Value: Select a file to upload

- **Analyze Responses:**
  - Check for success or error messages.

### **10. Update `app.py` for Enhanced Logging**

Consider adding more detailed logging within your Flask routes to capture and diagnose issues effectively.

**Example:**

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/upload', methods=['POST'])
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
        if not content:
            app.logger.error('No content extracted from the file')
            return jsonify({'error': 'No content extracted from the file'}), 400
        user_data = UserData(filename=file.filename, content=content)
        db.session.add(user_data)
        db.session.commit()
        app.logger.info(f'File {file.filename} uploaded successfully with ID {user_data.id}')
        return jsonify({'message': 'File uploaded successfully', 'user_data_id': user_data.id}), 200
    except Exception as e:
        app.logger.exception('An error occurred during file upload')
        return jsonify({'error': str(e)}), 500
```

## Project Structure

```
backend/
├── app.py
├── requirements.txt
├── config.py
├── models.py
├── utils.py
├── database.db
├── templates/
│   └── index.html
├── static/
│   └── styles.css
├── .env
└── README.md
```

- **`app.py`**: Main Flask application with API routes.
- **`requirements.txt`**: List of Python dependencies.
- **`config.py`**: Configuration settings for Flask and environment variables.
- **`models.py`**: Database models using SQLAlchemy.
- **`utils.py`**: Utility functions for text extraction and OpenAI API interactions.
- **`database.db`**: SQLite database file.
- **`templates/`**: HTML templates for Flask routes.
- **`static/`**: Static files (CSS, JavaScript) for Flask routes.
- **`.env`**: Environment variables (should be kept secret and not committed to version control).
- **`README.md`**: Project documentation.

## Next Steps

With the backend now capable of handling large documents through chunking, you can proceed with the following:

1. **Frontend Development:**
   - Develop the React frontend to interact with the backend API.
   - Implement features like file upload interface, selection of study material type, and display of generated content.

2. **User Authentication (Optional):**
   - Implement user registration and login to personalize study materials further.

3. **Enhance Error Handling:**
   - Improve error messages and user feedback mechanisms on both frontend and backend.

4. **Optimize OpenAI API Usage:**
   - Implement caching mechanisms to reduce redundant API calls.
   - Handle rate limits and implement retries with exponential backoff.

5. **Deploy the Application:**
   - Deploy the backend to a cloud platform (e.g., Heroku, AWS) for accessibility.
   - Set up a production-ready frontend deployment.

6. **Expand File Type Support:**
   - Add support for additional file formats like Word documents (`.docx`).

7. **Improve Text Processing:**
   - Implement more sophisticated text preprocessing to enhance the quality of generated study materials.

## License

This project is licensed under the [MIT License](LICENSE).

---

## Notes

- **Security:** Ensure that sensitive information like the `.env` file is not committed to version control. Use `.gitignore` to exclude it.
- **Scalability:** For production environments, consider using a more robust database system and implementing scalability features.
- **API Limits:** Be mindful of the OpenAI API usage limits and monitor your usage to avoid unexpected costs.

---

Feel free to reach out if you have any questions or need further assistance with your project!