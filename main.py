from text_to_speech import TextToSpeechProcessor
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import uuid

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def pdf_to_speech(pdf_file_path, output_gcs_uri):
    processor = TextToSpeechProcessor(
        pdf_path=pdf_file_path,
        project_id=os.getenv("PROJECT_ID"),
        location=os.getenv("LOCATION"),
        output_gcs_uri=output_gcs_uri
    )
    processor.process()

@app.route("/upload", methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return redirect(request.url)
    
    file = request.files['pdf_file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        unique_id = uuid.uuid4().hex
        output_gcs_uri = f"{os.getenv('OUTPUT_GCS_URI')}/output_{unique_id}.wav"
        
        pdf_to_speech(file_path, output_gcs_uri)
        
        # Render the result template with message
        return render_template('result.html', message=f'File successfully uploaded and processed. Output file: {output_gcs_uri}')
    
    return 'Invalid file type'

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

