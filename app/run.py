import os
import sys
sys.path.append('.')
from datetime import datetime
import werkzeug
from docx import Document
from flask import Flask, render_template, request, make_response, jsonify
from modules.tools import convert_docx

app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
UPLOAD_DIR = "data"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload_multipart():
    use_num_convert = eval(request.form.get('num'))
    use_eng_convert = eval(request.form.get('eng'))
    use_highlight = eval(request.form.get('highlight'))
    # ★ポイント3
    if 'uploadFile' not in request.files:
        make_response(jsonify({'result':'uploadFile is required.'}))

    file = request.files['uploadFile']
    fileName = file.filename
    if '' == fileName:
        make_response(jsonify({'result':'filename must not empty.'}))

    # ★ポイント4
    saveFileName = 'converted.docx'
    file.save(os.path.join(UPLOAD_DIR, saveFileName))

    #convert
    document = Document(os.path.join(UPLOAD_DIR, saveFileName))
    document, df = convert_docx(
                            document,
                            use_num_convert = use_num_convert,
                            use_eng_convert = use_eng_convert,
                            use_highlight = use_highlight                 
                        )
    document.save(os.path.join(UPLOAD_DIR, saveFileName))

    response = make_response()

    # ★ポイント2
    response.data = open(os.path.join(UPLOAD_DIR, saveFileName), "rb").read()

    # ★ポイント3
    downloadFileName = os.path.join(UPLOAD_DIR, saveFileName)  
    response.headers['Content-Disposition'] = 'attachment; filename=' + downloadFileName

    # ★ポイント4
    return response

@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    print("werkzeug.exceptions.RequestEntityTooLarge")
    return 'result : file size is overed.'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 8888, debug=True)