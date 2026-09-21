from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
from docx import Document


def extract_resume_text(file):
    """
    Extract text from PDF or DOCX resume.
    """

    if not file:
        return ""

    file_name = file.name.lower()

    # PDF
    if file_name.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    # DOCX
    elif file_name.endswith(".docx"):
        document = Document(file)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + " "

        return text

    return ""


def calculate_match(resume_text, job_description):
    """
    Compare resume text with job description
    and return a match percentage.
    """

    if not resume_text or not job_description:
        return 0

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    match_percentage = round(similarity * 100, 2)

    return match_percentage