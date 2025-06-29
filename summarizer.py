
import docx
import fitz  # PyMuPDF
from rake_nltk import Rake
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import os

def extract_text(file_path):
    """
    Extracts text from .txt, .docx, or .pdf files.
    """
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])

    elif file_path.endswith('.pdf'):
        doc = fitz.open(file_path)
        return "\n".join([page.get_text() for page in doc])

    return ""

def summarize_text(text, sentence_count=5):
    """
    Summarizes text using LSA summarizer from sumy.
    """
    if not text.strip():
        return "No text provided for summarization."

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)

    return " ".join(str(sentence) for sentence in summary)

def extract_keywords(text):
    """
    Extracts top keywords using RAKE.
    """
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:10]

def generate_wordcloud(text):
    """
    Generates and saves a word cloud image from the text.
    """
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    output_path = os.path.join('static', 'wordcloud.png')

    # Make sure the static directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    wordcloud.to_file(output_path)
    return output_path
