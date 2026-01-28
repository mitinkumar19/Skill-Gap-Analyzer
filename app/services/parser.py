import pypdf
import io
import re

class ParsingService:
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extract text from a PDF file in memory."""
        try:
            pdf_reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return ParsingService.clean_text(text)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

    @staticmethod
    def clean_text(text: str) -> str:
        """Basic text cleaning."""
        # Remove multiple newlines
        text = re.sub(r'\n+', '\n', text)
        # Remove special characters but keep punctuation useful for sentence splitting
        text = re.sub(r'[^\w\s.,;:()\-]', '', text)
        return text.strip()
