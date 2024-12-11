import os
from flask import Flask, request, render_template, redirect, url_for, flash

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Directory to save uploaded files
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # Allowed file types
app.secret_key = 'supersecretkey'  # For flashing messages

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper function to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home route with upload form
@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        # Check if files are in the POST request
        if 'files[]' not in request.files:
            flash('No files part in the request')
            return redirect(request.url)
        
        files = request.files.getlist('files[]')  # Get list of files
        if not files or all(file.filename == '' for file in files):
            flash('No selected files')
            return redirect(request.url)
        
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                uploaded_files.append(filename)
        
        if uploaded_files:
            flash(f'Successfully uploaded: {", ".join(uploaded_files)}')
        else:
            flash('No valid files to upload!')

        return redirect(url_for('upload_files'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
