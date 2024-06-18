# app.py

from flask import Flask, request, render_template
import os
from model.model import generate_caption

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(image_path)
            caption = generate_caption(image_path)
            return render_template('index.html', caption=caption, image_path=image_path)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
