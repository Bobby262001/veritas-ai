import pypdf
from fpdf import FPDF
import io
import re

def extract_text_from_pdf(pdf_file) -> list:
    """
    Extracts text from a PDF file object page by page.
    Returns a list of dictionaries with page numbers and text content.
    """
    pages_data = []
    try:
        # pdf_file can be a file-like object (e.g. Streamlit UploadedFile) or a file path
        reader = pypdf.PdfReader(pdf_file)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                # Basic cleaning of formatting issues
                text = re.sub(r'\r\n', '\n', text)
                pages_data.append({
                    "page_number": i + 1,
                    "text": text.strip()
                })
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {str(e)}")
    
    return pages_data

def clean_txt_for_latin1(text: str) -> str:
    """
    fpdf2 by default uses Latin-1 encoding for core fonts (Helvetica, Arial, etc.).
    This function cleans or replaces Unicode characters that aren't Latin-1 compatible
    to prevent PDF generation crashes.
    """
    # Replace common smart quotes, dashes, etc.
    replacements = {
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '-',
        '\u2022': '*', '\u2026': '...',
        '\xa0': ' '
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    
    # Encode to latin-1, replacing other characters with '?' to avoid exceptions
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_pdf_from_text(text: str) -> bytes:
    """
    Generates a PDF file (in-memory as bytes) from raw text.
    Uses clean formatting with margin wrapping.
    """
    # Clean text to prevent PDF encoding issues
    cleaned_text = clean_txt_for_latin1(text)
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Set title/header
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, "Processed Content Document", ln=True, align="C")
    pdf.ln(5)
    
    # Set body text
    pdf.set_font("Helvetica", size=11)
    
    # Split by newlines and print paragraph by paragraph
    paragraphs = cleaned_text.split('\n')
    for para in paragraphs:
        if para.strip():
            pdf.multi_cell(0, 6, para)
            pdf.ln(4)
        else:
            pdf.ln(2)
            
    # Output PDF as a byte string
    return pdf.output()
