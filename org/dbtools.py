from re import compile as R
from django.db import connection, transaction

is_SELECT=lambda sql:R(r"(?i)^\s*SELECT").match(sql)

def rawsql(columns, sql, params=None):
	cursor = connection.cursor()
	if params: cursor.execute(sql, params)
	else: cursor.execute(sql)
	if is_SELECT(sql):
		for row in cursor.fetchall():
			yield {columns[i]:row[i] for i in xrange(len(columns))}
	else: transaction.commit_unless_managed()
