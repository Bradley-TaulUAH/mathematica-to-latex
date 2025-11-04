"""
Mathematica to LaTeX/Markdown Converter - Web GUI
A web-based user interface for converting Mathematica notebooks
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile
import shutil
from mathematica_converter import MathematicaConverter
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

ALLOWED_EXTENSIONS = {'nb'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    """Handle file conversion request"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type. Please upload a .nb file'})
        
        # Get output format
        output_format = request.form.get('format', 'both')
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Create output directory
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Perform conversion
        converter = MathematicaConverter()
        success, message = converter.convert_file(input_path, output_format, output_dir)
        
        if success:
            # Get base filename without extension
            base_name = os.path.splitext(filename)[0]
            
            # Prepare file paths
            files = {}
            if output_format in ['latex', 'both']:
                latex_file = os.path.join(output_dir, f"{base_name}.tex")
                if os.path.exists(latex_file):
                    with open(latex_file, 'r', encoding='utf-8') as f:
                        files['latex'] = {
                            'filename': f"{base_name}.tex",
                            'content': f.read()
                        }
            
            if output_format in ['markdown', 'both']:
                markdown_file = os.path.join(output_dir, f"{base_name}.md")
                if os.path.exists(markdown_file):
                    with open(markdown_file, 'r', encoding='utf-8') as f:
                        files['markdown'] = {
                            'filename': f"{base_name}.md",
                            'content': f.read()
                        }
            
            return jsonify({
                'success': True,
                'message': message,
                'files': files
            })
        else:
            return jsonify({'success': False, 'error': message})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/download/<format_type>/<filename>')
def download(format_type, filename):
    """Download converted file"""
    try:
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
        file_path = os.path.join(output_dir, filename)
        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return "File not found", 404
            
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    print("Starting Mathematica to LaTeX/Markdown Converter Web GUI...")
    print("Open your browser and navigate to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
