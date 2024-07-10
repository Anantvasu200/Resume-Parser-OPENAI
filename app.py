import os
import sys
from flask import Flask, request, jsonify, render_template
from pypdf import PdfReader
import json
from resumeparser import ats_extractor

sys.path.insert(0, os.path.abspath(os.getcwd()))

UPLOAD_PATH = r"__DATA__"

# Ensure the UPLOAD_PATH directory exists
if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)

app = Flask(__name__)  # create the Flask app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def ats():
    doc = request.files['pdf_doc']
    doc.save(os.path.join(UPLOAD_PATH, "file.pdf"))
    doc_path = os.path.join(UPLOAD_PATH, "file.pdf")
    data = read_file_from_path(doc_path)
    extracted_data = ats_extractor(data)

    # Assuming ats_extractor returns a JSON string
    data = json.loads(extracted_data)

    return render_template('index.html', data=data)

def read_file_from_path(path):
    reader = PdfReader(path)
    data = ""

    for page_no in range(len(reader.pages)):
        data += reader.pages[page_no].extract_text()
    return data

if __name__ == '__main__':
    app.run(port=8000)  # run the Flask app
