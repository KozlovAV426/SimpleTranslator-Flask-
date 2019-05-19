import sqlite3

from work_with_database import get_rows_from_database, add_to_database, create_database

from py_translator import Translator

from flask import Flask, render_template, redirect, request
from config import Configuration, INPUT, TRANSLATION, LANGUAGE, LENGTH

app = Flask(__name__)
app.config.from_object(Configuration)

translation = ''
messages = []

create_database()


@app.route('/', methods=['GET'])
def index():
	messages.clear()
	translation = ''
	return render_template('index.html')


@app.route('/translator', methods=['GET'])
def translator():
	global translation
	return render_template('translator.html', messages=messages, content=translation)


@app.route('/translate', methods=['POST'])
def translate():

	text = request.form['text']
	language = request.form['lang']

	if len(text) == 0:
		return render_template('translator_wrong.html')

	global translation
	translation = Translator().translate(text=text, dest=language).text

	global messages
	messages.clear()

	add_to_database(text, translation, language, len(text))

	rows = get_rows_from_database()

	for i in range(len(rows) - 1, -1, -1):
		if (rows[i][LANGUAGE] == language):
			messages.append(rows[i])
			if (len(messages) == 5):
				break
	return redirect('translator')


@app.route('/database')
def database():
	rows = get_rows_from_database()
	return render_template('database.html', rows=rows)


@app.route('/statistics')
def statistics():
	rows = get_rows_from_database()
	statistics = dict()
	if len(rows) > 0:
		minlength = rows[0][LENGTH]
		minlength_request = rows[0]
		for row in rows:
			if row[LENGTH] < minlength:
				minlength = row[3]
				minlength_request = row
			if row[LANGUAGE] in statistics.keys():
				statistics[row[LANGUAGE]] += 1
			else:
				statistics[row[LANGUAGE]] = 1
		return render_template('get_statistics.html',
                         shortest_request=minlength_request, minlength=minlength, statistics=statistics,
                         amount=len(rows))
	else:
		return render_template('empty_statistics.html')


app.run()
