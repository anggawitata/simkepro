from flask import Flask, render_template, request
from controllers.process_controller import save_file, process_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file:
        filepath = save_file(file)

        preview, summary = process_file(filepath)

        return render_template(
            'result.html',
            preview=preview,
            summary=summary
        )

    return "Tidak ada file"

if __name__ == '__main__':
    app.run(debug=True)