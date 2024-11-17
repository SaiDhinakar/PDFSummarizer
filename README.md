# PDF Summarizer with Flask

This project is a PDF summarization application built with Flask. It allows users to upload PDF files, which are then processed and summarized. The summaries can be downloaded in either text or PDF format. The app uses SQLAlchemy for managing database interactions and stores basic analytics related to file uploads.

## Features

- **File Upload**: Users can upload PDF files which are stored on the server.
- **Summarization**: The uploaded PDF files are summarized using the `PDFSummarizer` module.
- **Download Summary**: Users can download the summarized content in either `.txt` or `.pdf` format.
- **Database**: Stores user credentials and file uploads, with some basic metadata like file size and upload time for future analysis.

## Requirements

To run this project, you'll need to have the following installed:

- Python 3.x
- Flask
- Flask-SQLAlchemy
- werkzeug
- xhtml2pdf
- other necessary libraries (listed below)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SaiDhinakar/PDFSummarizer.git
   cd pdf-summarizer-flask
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   The app uses SQLite for storing user and file upload information. It initializes the database the first time the app runs.

5. **Run the Flask app**:
   ```bash
   python app.py
   ```
   The application will be available at `http://127.0.0.1:5000/`.

## Project Structure

```
/pdf-summarizer-flask
│
├── app.py                 # Main application file
├── /uploads               # Directory where uploaded PDFs are stored
├── /templates             # HTML templates for rendering the web pages
│   ├── index.html         # Home page for uploading PDFs
│   └── summary.html       # Page for displaying summarized PDF
├── /static                # CSS, JavaScript, and other static files
├── /summarizer_.py        # Custom Python module for PDF summarization
├── requirements.txt       # List of Python dependencies
└── README.md              # This file
```

## Routes

- `/`: The homepage where users can upload PDFs.
- `/upload`: Handles the upload and storage of PDFs.
- `/summarize/<filename>`: Displays the summarized content of the uploaded PDF.
- `/download/<file_format>`: Allows users to download the summary in `.txt` or `.pdf` format.


## Database Models

The application uses SQLAlchemy and SQLite to manage the following models:

- **User**: Stores user credentials (username and password).
- **Upload**: Stores information about uploaded PDFs, such as filename, file size, and upload timestamp.

## Dependencies

- Flask: The web framework for building the application.
- Flask-SQLAlchemy: SQLAlchemy ORM integration for Flask.
- werkzeug: Provides utilities for handling file uploads.
- xhtml2pdf: Converts HTML summaries to PDF format.
- Other Python libraries for functionality like datetime, os, etc.

## Usage

1. **Uploading PDFs**: After logging in, users can upload PDF files, which will be processed and summarized.
2. **Viewing Summary**: Once the PDF is summarized, users will be redirected to a page where the summary is displayed.
3. **Downloading Summary**: The summary can be downloaded in text (`.txt`) or PDF (`.pdf`) format by clicking the respective download buttons.

## Future Improvements

- Add password hashing for user authentication for better security.
- Enhance PDF summarization capabilities.
- Provide more detailed analytics on file uploads and summarizations.
- Implement user roles and permissions for additional functionality.

