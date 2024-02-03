from flask import Flask, session, render_template, Response, request, request, url_for, flash, redirect
# from generate_content import *
import re

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        pass

    return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True)
