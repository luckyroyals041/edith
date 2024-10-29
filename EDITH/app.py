from flask import Flask, render_template, request, jsonify, send_file
import sys
import os

# Set up the path to find local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import module functions
from FileOrganizer.file_org import organize_files
from QRGenerator.qr_gen import generate_qr

app = Flask(__name__)

# Configure app settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'static', 'qr_codes')

# Ensure required directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Route handlers
@app.route('/')
def home():
    """Render the main dashboard page"""
    return render_template('index.html')

@app.route('/file-organizer')
def file_organizer():
    """Render the file organizer page"""
    return render_template('file_organizer.html')

@app.route('/qr-generator')
def qr_generator():
    """Render the QR generator page"""
    return render_template('qr_generator.html')

@app.route('/organize', methods=['POST'])
def organize():
    """Handle file organization requests"""
    data = request.json
    directory = data.get('directory')
    
    if not directory:
        return jsonify({
            'status': 'error',
            'message': 'No directory provided'
        })
    
    try:
        # Print debug information
        print(f"Received directory path: {directory}")
        
        # Normalize the path (handle both forward and back slashes)
        directory = os.path.normpath(directory)
        
        # Convert to absolute path if not already
        if not os.path.isabs(directory):
            directory = os.path.abspath(directory)
        
        print(f"Normalized directory path: {directory}")
        
        # Verify the directory exists
        if not os.path.exists(directory):
            return jsonify({
                'status': 'error',
                'message': f'Directory does not exist: {directory}'
            })
            
        if not os.path.isdir(directory):
            return jsonify({
                'status': 'error',
                'message': f'Path is not a directory: {directory}'
            })
            
        result = organize_files(directory)
        return jsonify({
            'status': 'success',
            'message': result
        })
        
    except PermissionError:
        return jsonify({
            'status': 'error',
            'message': 'Permission denied. Please check folder permissions.'
        })
    except Exception as e:
        print(f"Error organizing files: {str(e)}")  # Debug log
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        })

@app.route('/generate-qr', methods=['POST'])
def qr_endpoint():
    """Handle QR code generation requests"""
    data = request.json
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({
            'status': 'error',
            'message': 'No text provided'
        }), 400
    
    try:
        qr_image = generate_qr(text)
        return jsonify({
            'status': 'success',
            'qr_image': qr_image
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to generate QR code: {str(e)}'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# Development server configuration
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Make server accessible externally
        port=5000,       # Port to run the server on
        debug=True       # Enable debug mode for development
    )
