# summarizer.py
from summarizer import Summarizer
import PyPDF2

class PDFSummarizer:
    def __init__(self):
        pass
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return None
        return text
    
    def summarize(self, pdf_path):
        """Main function to extract text and generate summary"""
        try:
            # Extract text from PDF
            text = self.extract_text_from_pdf(pdf_path)
            if text is None or text.strip() == "":
                return "No text extracted from PDF or PDF is empty."
            
            summy = Summarizer()
            # Generate summary using your module
            summary = summy(text)  # Ensure this call is correct based on your summarizer's API
            
            return summary
            
        except Exception as e:
            print(f"Error in summarization process: {str(e)}")
            return f"Error generating summary: {str(e)}"
            