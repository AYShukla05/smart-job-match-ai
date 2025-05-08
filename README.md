# 🔍 Smart Job Match AI – Resume and Job Skill Analyzer (CLI Tool)

A command-line AI tool that analyzes resumes, compares them against job descriptions, identifies skill gaps, and recommends personalized learning paths. Built for AI/ML learners preparing for job roles like NLP Engineer, ML Engineer, or Prompt Engineer.

## 🚀 Features

- ✅ Resume parsing from PDF/DOCX
- ✅ Job description parsing from CSV or text
- ✅ Semantic skill matching using SBERT (sentence-transformers)
- ✅ Skill gap detection with learning recommendations (Coursera/GitHub)
- ✅ Optional GPT-based career prompt generator
- ✅ CLI output in Markdown, JSON, CSV formats

---

## 📂 Project Structure
smart_job_match_ai/
├── main.py                       # CLI entry point
├── parsers/                     # Resume & job description loaders
├── matching/                    # Embedding and skill comparison logic
├── recommender/                 # Skill gap and learning suggestions
├── prompts/                     # GPT-based career advisor (optional)
├── reports/                     # Markdown / JSON / CSV report generators
├── tests/                       # Unit tests
├── requirements.txt             # Python dependencies

---

## 🧠 Skills You'll Learn (By Building or Using It)

- Python (file handling, modular CLI development)
- Natural Language Processing (spaCy, regex, NER)
- Semantic embeddings (BERT, SBERT)
- Cosine similarity for job matching
- Prompt engineering for GPT
- Report formatting for technical analysis

---

## 🛠️ Installation

```bash
git clone git@github.com:hshukla4/smart-job-match-ai.git
cd smart-job-match-ai
pip install -r requirements.txt


# Run full analysis
python main.py --resume ./docs/resume.pdf --jobs ./data/jobs.csv --output ./reports/

# View missing skills & learning plan
python main.py --skills-recommend

# Generate GPT-based career guidance (optional)
python main.py --career-advice
