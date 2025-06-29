from flask import Flask, request, render_template, send_file
from summarizer import extract_text, summarize_text, extract_keywords, generate_wordcloud
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    keywords = []
    wordcloud_path = None

    if request.method == 'POST':
        file = request.files['file']
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        full_text = extract_text(filepath)
        summary = summarize_text(full_text)
        keywords = extract_keywords(full_text)
        wordcloud_path = generate_wordcloud(full_text)

    return render_template("index.html", summary=summary, keywords=keywords, wordcloud_path=wordcloud_path)


if __name__ == '__main__':
    app.run(debug=True)