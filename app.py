import sqlite3

from work_with_database import get_rows_from_database, add_to_database, create_database

from py_translator import Translator

from flask import Flask, render_template, redirect, request
from config import Configuration, INPUT, TRANSLATION, LANGUAGE, LENGTH, MAX_LAST_REQUEST_COUNTER 

app = Flask(__name__)
app.config.from_object(Configuration)

create_database()


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


def translate_redirector(text=' ', language='en', show_previous=False):
	if len(text) == 0:
		return render_template('translator_wrong.html')

	translation = Translator().translate(text=text, dest=language).text
	messages = []

	if (show_previous):
		add_to_database(text, translation, language, len(text))
		rows = get_rows_from_database()
		for i in range(len(rows) - 1, -1, -1):
			if (rows[i][LANGUAGE] == language):
				messages.append(rows[i])
				if (len(messages) == MAX_LAST_REQUEST_COUNTER):
					break

	return render_template('translator.html', messages=messages, content=translation)



@app.route('/translator', methods=['GET'])
def translator():
	return translate_redirector()


@app.route('/translation_query', methods=['POST'])
def translate():

	text = request.form.get('text')
	language = request.form.get('lang')
	return translate_redirector(text, language, True)


@app.route('/database')
def database():
	rows = get_rows_from_database()
	return render_template('database.html', rows=rows)


@app.route('/statistics')
def statistics():
	rows = get_rows_from_database()
	statistics = {}
	if len(rows) > 0:
		minlength = rows[0][LENGTH]
		minlength_request = rows[0]
		for row in rows:
			if row[LENGTH] < minlength:
				minlength = row[LENGTH]
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
