import sqlite3


def get_rows_from_database():
	con = sqlite3.connect("database.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("select * from translations")
	frows = cur.fetchall()
	con.close()
	return frows


def add_to_database(text, translation, lang, length):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("INSERT INTO translations ( text, translation, lang, length) VALUES ( ?, ?, ?, ?)",
             (text, translation, lang, length))
	con.commit()
	con.close()


def create_database():
	conn = sqlite3.connect('database.db')
	#conn.execute("DROP TABLE translations")
	conn.execute('Create TABLE if not exists translations ( text TEXT, translation TEXT, lang TEXT, length INT)')
	conn.close()
