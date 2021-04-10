import os
import sys
sys.path.append('.')
from datetime import datetime
import werkzeug
from docx import Document
from flask import Flask, render_template, request, make_response, jsonify
from modules.tools import convert_docx, save_as_html

app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
UPLOAD_DIR = "data"
STATIC_DIR = "app/static"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload_multipart():
    use_num_convert = eval(request.form.get('num'))
    use_eng_convert = eval(request.form.get('eng'))
    use_highlight = eval(request.form.get('highlight'))

    if 'uploadFile' not in request.files:
        make_response(jsonify({'result':'uploadFile is required.'}))

    file = request.files['uploadFile']
    fileName = file.filename
    if '' == fileName:
        make_response(jsonify({'result':'filename must not empty.'}))

    orginal = 'original.docx'
    file.save(os.path.join(UPLOAD_DIR, orginal))
    save_as_html(os.path.join(UPLOAD_DIR, orginal), 'app/static/')

    #convert
    converted = 'converted.docx'
    document = Document(os.path.join(UPLOAD_DIR, orginal))
    document, df = convert_docx(
                            document,
                            use_num_convert = use_num_convert,
                            use_eng_convert = use_eng_convert,
                            use_highlight = use_highlight                 
                        )
    document.save(os.path.join(UPLOAD_DIR, converted))

    #save as html
    save_as_html(os.path.join(UPLOAD_DIR, converted), 'app/static/')

    response = make_response()

    response.data = open(os.path.join(UPLOAD_DIR, converted), "rb").read()

    # ★ポイント3
    downloadFileName = os.path.join(UPLOAD_DIR, converted)  
    response.headers['Content-Disposition'] = 'attachment; filename=' + downloadFileName

    # ★ポイント4
    return response

@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    print("werkzeug.exceptions.RequestEntityTooLarge")
    return 'result : file size is overed.'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 8888, debug=True)