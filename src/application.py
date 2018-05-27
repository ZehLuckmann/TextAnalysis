from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import AnalyzeConversation
import re

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.secret_key = "any random string"

db = SQLAlchemy(app)

import models

db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    errors = []
    words_frequencies = []
    file_title = "Nenhum arquivo selecionado"
    height = 450
    if request.method == 'POST':
        if 'entrada' not in request.files:
            errors.append("Arquivo de entrada precisa ser informado")
        else:
            file = request.files['entrada']
            if file.filename == '':
                errors.append("Arquivo de entrada inválido")

        if request.form.get("number") == "":
            errors.append("Número de palavras precisa ser informado")
        else:
            number_words = request.form.get("number")
            if not number_words.isdigit():
                errors.append("Número de palavras inválido")


        if (len(errors) == 0):
            an = AnalyzeConversation(file)
            an.load_stop_words()
            an.start_analyze()
            words_frequencies = an.get_result(int(number_words))
            height = len(words_frequencies) * 30
            file_title = file.filename

    return render_template("analyze.html", words_frequencies=words_frequencies, height = height,file_title=file_title, errors=errors)

app.run(host='0.0.0.0', port=8080, debug=True)
