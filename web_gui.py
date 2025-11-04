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
        success, _ = converter.convert_file(input_path, output_format, output_dir)
        
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
            
            # Don't expose internal file paths to users
            return jsonify({
                'success': True,
                'message': 'Conversion successful!',
                'files': files
            })
        else:
            # Don't expose internal error details to users
            return jsonify({'success': False, 'error': 'Conversion failed. Please check your file format and try again.'})
            
    except Exception:
        # Don't expose stack trace details to users
        return jsonify({'success': False, 'error': 'An error occurred during conversion. Please check your file and try again.'})


@app.route('/download/<format_type>/<filename>')
def download(format_type, filename):
    """Download converted file"""
    try:
        # Sanitize filename to prevent path traversal
        safe_filename = secure_filename(filename)
        if not safe_filename or safe_filename != filename:
            return "Invalid filename", 400
        
        # Only allow specific format types
        if format_type not in ['latex', 'markdown']:
            return "Invalid format type", 400
        
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
        file_path = os.path.join(output_dir, safe_filename)
        
        # Verify the path is within the output directory (prevent directory traversal)
        if not os.path.abspath(file_path).startswith(os.path.abspath(output_dir)):
            return "Invalid file path", 400
        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=safe_filename)
        else:
            return "File not found", 404
            
    except Exception:
        # Don't expose stack trace to users
        return "An error occurred during download", 500


if __name__ == '__main__':
    print("Starting Mathematica to LaTeX/Markdown Converter Web GUI...")
    print("Open your browser and navigate to: http://localhost:5000")
    app.run(debug=False, host='127.0.0.1', port=5000)
