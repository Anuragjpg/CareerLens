"""
Resume Parser Module
Extracts text from PDF resume files using pdfplumber.
"""

import pdfplumber


def extract_text_from_pdf(pdf_path):
    """
    Opens a PDF file and extracts all text from every page.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: Extracted text from PDF, or error message
    """
    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"[PDF] Reading {total_pages} page(s)...")

            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    print(f"[PDF] Page {i+1}: {len(page_text)} characters extracted")
                else:
                    print(f"[PDF] Page {i+1}: No text found (might be image)")

        if not text.strip():
            return "ERROR: No text could be extracted. PDF might be a scanned image."

        return text.strip()

    except Exception as e:
        print(f"[PDF ERROR] {str(e)}")
        return f"ERROR: Could not read PDF. Details: {str(e)}"


def get_word_count(text):
    """Count number of words in text"""
    if not text or text.startswith("ERROR"):
        return 0
    return len(text.split())


def get_basic_info(text):
    """Extract basic info like email and phone (optional helper)"""
    import re

    email = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone = re.findall(r'(?:\+91[\s-]?)?[6-9]\d{9}', text)

    return {
        "email": email[0] if email else "Not found",
        "phone": phone[0] if phone else "Not found"
    }