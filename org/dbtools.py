from django.db import connection

def rawsql(columns, sql, params=None):
	cursor = connection.cursor()
	if params: cursor.execute(sql, params)
	else: cursor.execute(sql)
	for row in cursor.fetchall():
		yield {columns[i]:row[i] for i in xrange(len(columns))}
