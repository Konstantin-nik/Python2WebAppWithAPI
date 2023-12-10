from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    text_to_translate = request.form['text_to_translate']
    target_language = request.form['target_language']


if __name__ == '__main__':
    app.run(debug=True)
