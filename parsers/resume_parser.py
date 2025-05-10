"""
resume_parser.py

A simple, modular resume parser for PDF and DOCX files.  
Uses PyMuPDF for PDFs and python-docx for Word documents,  
then applies text cleaning and section-based extraction  
to pull out name, contact info, education, skills, experience, projects, and publications.
"""

import fitz    # PyMuPDF
import docx    # python-docx

from utils import (
    clean_text,
    extract_name,
    extract_email,
    extract_phone,
    extract_sections_by_headings,
    parse_education,
    parse_skills,
    parse_experience,
    parse_projects,
    parse_publications
)


def extract_text_from_pdf(path):
    """
    Read and extract all text from each page of a PDF file.
    
    Args:
        path (str): filesystem path to the .pdf file.
    
    Returns:
        str: concatenated text of all pages, separated by newlines.
    """
    text = []
    with fitz.open(path) as pdf:
        for page in pdf:
            # get_text() returns the page’s text content
            text.append(page.get_text())
    return "\n".join(text)


def extract_text_from_docx(path):
    """
    Read and extract all text from a .docx Word document.
    
    Args:
        path (str): filesystem path to the .docx file.
    
    Returns:
        str: concatenated text of all paragraphs, separated by newlines.
    """
    doc = docx.Document(path)
    paragraphs = [para.text for para in doc.paragraphs]
    return "\n".join(paragraphs)


def parse_resume(path):
    """
    Orchestrate the full resume parsing pipeline:
      1) Read raw embedded text from PDF or DOCX.
      2) Clean up whitespace and punctuation.
      3) Extract top‐level fields (name, email, phone).
      4) Split text into logical sections by heading keywords.
      5) Post‐process each section into structured lists or dicts.
    
    Args:
        path (str): filesystem path to the resume file (.pdf or .docx).
    
    Returns:
        dict: parsed fields with keys:
            - name (str or None)
            - email (str or None)
            - phone (str or None)
            - education (List[str])
            - skills (List[str])
            - experience (List[dict])
            - projects (List[str])
            - publications (List[str])
    """
    # 1) Load raw text from the appropriate file type
    if path.lower().endswith('.pdf'):
        raw_text = extract_text_from_pdf(path)
    elif path.lower().endswith('.docx'):
        raw_text = extract_text_from_docx(path)
    else:
        raise ValueError("Unsupported format: only .pdf and .docx are accepted")

    # 2) Normalize spacing, remove smart quotes, unify line breaks
    cleaned = clean_text(raw_text)

    # 3) Extract contact and identity fields
    name  = extract_name(cleaned)
    email = extract_email(cleaned)
    phone = extract_phone(cleaned)

    # 4) Break the document into named sections
    sections = extract_sections_by_headings(cleaned)

    # 5) Parse each section into the desired structure
    education    = parse_education(sections.get('education', []))
    skills       = parse_skills(sections.get('skills', []))
    experience   = parse_experience(sections.get('experience', []))
    projects     = parse_projects(sections.get('projects', []))
    publications = parse_publications(sections.get('publications', []))

    # 6) Assemble the final result
    return {
        'name':         name,
        'email':        email,
        'phone':        phone,
        'education':    education,
        'skills':       skills,
        'experience':   experience,
        'projects':     projects,
        'publications': publications
    }


if __name__ == '__main__':
    import json
    result = parse_resume('sample_resume_multi.pdf')
    print(json.dumps(result, indent=2))
