# utils.py

import re

# Map logical sections to their possible header keywords
SECTION_HEADERS = {
    'summary':      ['summary'],
    'skills':       ['skills', 'technical skills', 'competencies', 'expertise'],
    'experience':   ['experience', 'work history', 'professional background', 'career highlights'],
    'projects':     ['projects', 'portfolio', 'technical projects'],
    'publications': ['publications', 'papers', 'articles', 'research'],
    'education':    ['education', 'academic background', 'degrees']
}

def clean_text(text):
    """
    Normalize whitespace and punctuation.
    """
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'[“”]', '"', text)
    text = re.sub(r"[‘’]", "'", text)
    return text.strip()

def extract_name(text):
    """
    Return first non-blank line that doesn't look like contact info.
    """
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        low = line.lower()
        if 'email' in low or 'phone' in low or 'location' in low:
            continue
        return line
    return None

def extract_email(text):
    """
    Return first email found, or None.
    """
    m = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return m.group(0) if m else None

def extract_phone(text):
    """
    Return first phone number found (intl/local), or None.
    """
    m = re.search(r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}', text)
    return m.group(0) if m else None

def extract_sections_by_headings(text):
    """
    Split text into lines, detect section headers by keyword,
    and collect all subsequent non-blank lines until the next header.
    """
    sections = {name: [] for name in SECTION_HEADERS}
    current = None
    for line in text.split('\n'):
        low = line.lower()
        # detect header
        for sec, keys in SECTION_HEADERS.items():
            if any(k in low for k in keys):
                current = sec
                break
        else:
            if current and line.strip():
                sections[current].append(line)
    return sections

def strip_bullet(line):
    return re.sub(r'^[\-\*\u2022]\s*', '', line).strip()

def parse_education(lines):
    """
    Strip bullets from each education entry.
    """
    return [strip_bullet(l) for l in lines]

def parse_skills(lines):
    """
    Split on commas/slashes/and, strip bullets and labels, dedupe.
    """
    items = []
    for ln in lines:
        ln = strip_bullet(ln)
        ln = re.sub(r'^\w+:\s*', '', ln)  # remove labels like "Programming:"
        for part in re.split(r',|/|\band\b', ln):
            p = part.strip()
            if p and p not in items:
                items.append(p)
    return items

def parse_experience(lines):
    """
    Group job titles (non-bullets) with their following bullet details.
    """
    experiences = []
    current = None
    for ln in lines:
        if not ln.lstrip().startswith(('-', '*', '•')):
            # new title
            if current:
                experiences.append(current)
            current = {'title': ln.strip(), 'details': []}
        else:
            # bullet detail
            if current:
                current['details'].append(strip_bullet(ln))
    if current:
        experiences.append(current)
    return experiences

def parse_projects(lines):
    """
    Strip bullets, then merge continuation lines into the last project.
    """
    projects = []
    for ln in lines:
        if ln.lstrip().startswith(('-', '*', '•')):
            # new project
            projects.append(strip_bullet(ln))
        else:
            # continuation of last
            if projects:
                projects[-1] += ' ' + ln.strip()
    return projects

def parse_publications(lines):
    """
    Strip bullets or numbering, merge wrapped lines.
    """
    pubs = []
    for ln in lines:
        # remove leading number/bullet
        clean = re.sub(r'^(?:\d+\.\s*|[\-\*\u2022]\s*)', '', ln).strip()
        if ln.lstrip().startswith(('-', '*', '•')) or re.match(r'^\d+\.', ln):
            pubs.append(clean)
        else:
            if pubs:
                pubs[-1] += ' ' + ln.strip()
    return pubs
