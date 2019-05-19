import sqlite3
from contextlib import closing


def get_rows_from_database():
	with closing(sqlite3.connect('database.db')) as con:
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute("select * from translations")
		frows = cur.fetchall()
	return frows


def add_to_database(text, translation, lang, length):
	with closing(sqlite3.connect('database.db')) as con:
		cur = con.cursor()
		cur.execute("INSERT INTO translations ( text, translation, lang, length) VALUES ( ?, ?, ?, ?)",
             (text, translation, lang, length))
		con.commit()


def create_database():
	with closing(sqlite3.connect('database.db')) as con:
		#con.execute("DROP TABLE translations")
	  con.execute('Create TABLE if not exists translations ( text TEXT, translation TEXT, lang TEXT, length INT)')
