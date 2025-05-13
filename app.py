from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
from utils.process_excel import extract_vin_tasks
from utils.generate_pdf import create_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PDF_FOLDER'] = 'static/pdf'

# Crée les dossiers s'ils n'existent pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PDF_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.xlsx'):
        return jsonify({'success': False, 'error': 'Fichier non valide. Veuillez fournir un fichier Excel .xlsx'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        vin_data = extract_vin_tasks(filepath)
        pdf_filenames = create_pdf(vin_data, output_dir=app.config['PDF_FOLDER'])

        pdf_urls = [f"/download/{name}" for name in pdf_filenames]

        return jsonify({
            'success': True,
            'pdf_urls': pdf_urls,
            'vin_tasks': vin_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['PDF_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
