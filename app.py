from flask import Flask, session, render_template, Response, request, request, url_for, flash, redirect
from extract_paragraphs import *
import re

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

appName = "Journey"

pages = split_pdf("harrypotter.pdf")

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        pass

    return render_template('index.html', appName=appName, pages=pages)

if __name__ == "__main__":
  app.run(debug=True)
