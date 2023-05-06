# run from browser

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['audio']
        # Do something with the audio file, such as save it to disk or process it
        return 'Audio file received'
    return '''
        <!doctype html>
        <html>
            <body>
                <h1>Upload an audio file</h1>
                <form method="POST" enctype="multipart/form-data">
                    <input type="file" name="audio">
                    <input type="submit" value="Upload">
                </form>
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
