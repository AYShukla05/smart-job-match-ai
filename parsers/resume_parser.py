"""
Improved Resume Parser Script
-----------------------------
Extracts structured data from resumes:
- Email, phone, skills
- Education (with degree + institution)
- Certifications (no section headers)
- Experience (role + bullets)
- Projects (only under Projects section)
- Publications (only under Publications section)
- References
"""

import fitz  # PyMuPDF
import docx
import re
import pytesseract

# Set the path to the tesseract.exe inside your repo folder
pytesseract.pytesseract.tesseract_cmd = r'E:\AI&DS\SmartJobMatchAI\smart-job-match-ai-main\tesseract\tesseract.exe'

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None


def extract_phone(text):
    match = re.search(r'\+?\d[\d -]{8,}\d', text)
    return match.group(0) if match else None


def extract_skills(text, skills_list):
    return [skill for skill in skills_list if skill.lower() in text.lower()]


def extract_education(text):
    lines = text.split('\n')
    education = []
    for line in lines:
        if re.search(r'(Bachelor|Master|PhD|B\.Sc|M\.Sc|B\.Tech|M\.Tech).*?,', line, re.IGNORECASE):
            education.append(line.strip())
    return education


def extract_section_block(text, section_title):
    """
    Extract lines under a specific section until the next section or empty line.
    """
    lines = text.split('\n')
    block = []
    capture = False
    for line in lines:
        if section_title.lower() in line.lower():
            capture = True
            continue
        if capture:
            if line.strip() == '' or re.match(r'^[A-Za-z ]+:$', line.strip()):  # Next section header
                break
            block.append(line.strip())
    return block


def extract_certifications(text):
    return extract_section_block(text, 'Certifications')


def extract_experience(text):
    lines = text.split('\n')
    experience = []
    capture = False
    for line in lines:
        # Only start capturing when hitting exact section header 'Experience:'
        if line.strip().lower() == 'experience:':
            capture = True
            continue
        if capture:
            # Stop at next section header (line ending with ':') or blank line
            if line.strip() == '' or re.match(r'^[A-Za-z ]+:$', line.strip()):
                break
            # Capture non-empty lines
            if line.strip():
                experience.append(line.strip())
    return experience


def extract_projects(text):
    return extract_section_block(text, 'Projects')


def extract_publications(text):
    return extract_section_block(text, 'Publications')


def extract_references(text):
    if 'References' in text:
        return ['Available upon request']
    return []


def parse_resume(file_path):
    skills_list = ['Python', 'Java', 'Machine Learning', 'Data Analysis', 'SQL',
                   'Pandas', 'NumPy', 'Scikit-learn', 'Flask']

    # Extract raw text
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type")

    print("Extracted Text:", text)  # Debugging line to check extracted text
    # Extract fields
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text, skills_list)
    education = extract_education(text)
    certifications = extract_certifications(text)
    experience = extract_experience(text)
    projects = extract_projects(text)
    publications = extract_publications(text)
    references = extract_references(text)

    result = {
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "certifications": certifications,
        "experience": experience,
        "projects": projects,
        "publications": publications,
        "references": references
    }

    return result


if __name__ == "__main__":
    test_file = "sample_resume.pdf"  # Replace with your test file path
    parsed_data = parse_resume(test_file)
    print("Parsed Resume Data:")
    for key, value in parsed_data.items():
        print(f"{key.capitalize()}: {value}")
