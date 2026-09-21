# JobPortal

A Django-based Job Portal that allows users to discover jobs, create accounts, apply for jobs, upload resumes, and receive an AI-based resume-to-job matching score.

## 🚀 Features

- User registration and login
- Job search by title and location
- Job details page
- Online job application
- Resume upload with PDF/DOCX support
- Duplicate application prevention
- Phone number validation
- Application success page
- Admin panel for managing jobs and applications
- Resume access from the admin panel
- External job listings using Adzuna API
- AI-powered Resume–Job Matching
- Match percentage using TF-IDF and Cosine Similarity
- Light/Dark theme support

## 🤖 AI Resume–Job Matching

The application compares the uploaded resume with the selected job description using Natural Language Processing.

### How it works

1. Resume text is extracted from PDF or DOCX.
2. TF-IDF converts the resume and job description into numerical vectors.
3. Cosine Similarity compares the two vectors.
4. The similarity score is converted into a percentage.
5. The match percentage is stored with the application and displayed to the user.

> The match percentage represents textual similarity between the resume and job description. It is not a guarantee of candidate qualification.

## 🛠️ Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript
- Scikit-learn
- PyPDF
- python-docx
- Requests
- Adzuna Jobs API
- Git & GitHub

## 📂 Project Structure

```text
JobPortal/
│
├── invoices/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── ai_matcher.py
│   ├── forms.py
│   ├── models.py
│   └── views.py
│
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md