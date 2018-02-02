from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html.j2')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
