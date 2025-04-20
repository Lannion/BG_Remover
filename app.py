from flask import Flask, render_template, request
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

# Folder to store processed images
OUTPUT_FOLDER = 'static/output'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('image')

        if file:
            try:
                input_image = Image.open(file).convert("RGBA")
                output_image = remove(input_image)

                # Clean filename
                filename = file.filename.replace(" ", "_")
                output_path = os.path.join(OUTPUT_FOLDER, filename)
                output_image.save(output_path)

                return render_template('index.html', output_image=filename) 
            except Exception as e:
                print("Error processing image:", e)
                return render_template('index.html', output_image=None)

    return render_template('index.html', output_image=None)

if __name__ == '__main__':
    app.run(debug=True)
