
from flask import Flask, render_template, request
from google import genai
from google.genai import types
import PIL.Image
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Configure Google Gemini client
api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

@app.route('/')
def index():
    return '''
    <h1>Drag and Drop an Image for Analysis</h1>
    <form action="/analyze" method="post" enctype="multipart/form-data" id="uploadForm">
        <div id="dropArea" style="border: 2px dashed #ccc; padding: 50px; text-align: center;">
            Drag and drop an image here or click to select
            <input type="file" name="file" accept="image/*" required style="display: none;">
        </div>
        <br>
        <p id="confirmation" style="display: none; color: green;">Image uploaded successfully!</p>
        <input type="submit" value="Analyze Image" id="submitButton">
        <p id="processing" style="display: none;">Processing...</p>
    </form>

    <script>
        const dropArea = document.getElementById('dropArea');
        const fileInput = dropArea.querySelector('input[type="file"]');
        const confirmation = document.getElementById('confirmation');
        const submitButton = document.getElementById('submitButton');
        const processing = document.getElementById('processing');

        dropArea.addEventListener('click', () => fileInput.click());

        dropArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropArea.style.border = '2px solid #000';
        });

        dropArea.addEventListener('dragleave', () => {
            dropArea.style.border = '2px dashed #ccc';
        });

        dropArea.addEventListener('drop', (e) => {
            e.preventDefault();
            dropArea.style.border = '2px dashed #ccc';
            const file = e.dataTransfer.files[0];
            fileInput.files = e.dataTransfer.files;
            confirmation.style.display = 'block';
        });

        submitButton.addEventListener('click', () => {
            processing.style.display = 'block';
        });
    </script>
    '''

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    # Save uploaded file
    filepath = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(filepath)

    # Process the image using Google Gemini
    image = PIL.Image.open(filepath)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["This is an image from my lecture. Can you please explain it to me in detail and simple terms", image]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"Can make a beautiful and presentable Website using the following content and return JUST the html code for the same. make it colorful and non boring but not too flashy. content : {response.text}"]
    )

    # Get and display the output
    output_text = response.text
    return output_text

if __name__ == '__main__':
    app.run(debug=True)

