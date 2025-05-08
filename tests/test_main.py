# Basic test cases for CLI and modules
# test_run.py
from parsers.resume_parser import parse_resume
from parsers.job_parser import load_jobs

resume_text = parse_resume("docs/resume.pdf")
jobs = load_jobs("data/jobs.csv")

print("Extracted Resume Text:", resume_text[:500])
print("Loaded Jobs:", jobs)
