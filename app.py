from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from summarizer_ import PDFSummarizer
from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["UPLOAD_FOLDER"] = "uploads/"
app.config["ALLOWED_EXTENSIONS"] = {"pdf"}
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///analytics.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Store file size in bytes
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_request
def setup_db():
    if not getattr(app, '_db_initialized', False):  # Run once
        db.create_all()
        app._db_initialized = True


# Helper: Check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file part.")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file.")
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Get file size in bytes
        file_size = os.path.getsize(file_path)  # File size in bytes

        # Save upload details to DB
        upload = Upload(filename=filename, file_size=file_size)
        db.session.add(upload)
        db.session.commit()

        return redirect(url_for("summarize_pdf", filename=filename))

    flash("Invalid file type. Only PDFs are allowed.")
    return redirect(url_for("index"))

@app.route("/summarize/<filename>")
def summarize_pdf(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    summarizer = PDFSummarizer()
    summary = summarizer.summarize(file_path)

    # Save summary in session
    session["summary"] = summary

    return render_template("summary.html", filename=filename, summary=summary)

@app.route('/download/<file_format>')
def download_summary(file_format):
    summary = session.get('summary', 'No summary available')

    if file_format == 'txt':
        return send_file(BytesIO(summary.encode()), as_attachment=True, download_name="summary.txt", mimetype="text/plain")
    
    elif file_format == 'pdf':
        pdf = BytesIO()
        pisa.CreatePDF(BytesIO(f"<h1>Summarized Text</h1><p>{summary}</p>".encode()), pdf)
        pdf.seek(0)
        return send_file(pdf, as_attachment=True, download_name="summary.pdf", mimetype="application/pdf")
    
    return "Invalid file format", 400


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials.")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True)
