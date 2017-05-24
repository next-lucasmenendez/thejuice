import os
import sys
import sqlite3
from configparser import ConfigParser

class DB:
	def __init__(self):
		main_path = os.path.realpath(sys.argv[0])
		path, runfile = os.path.split(main_path)

		config	= ConfigParser()
		file	= '%s/config.ini' % path

		config.read(file)
		name = config.get('database', 'file')

		self.database = "{}/{}".format(path, name)
		self.connection = None
		self.cursor = None
		self.lastid = -1

	def __dictfactory(self, cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

	def __verify(*inputs):
		result = True
		for x in inputs:
			result = result and bool(x)

		return result

	def connect(self):
		try:
			self.connection = sqlite3.connect(self.database)
			self.connection.row_factory = self.__dictfactory
			self.cursor = self.connection.cursor()
		except sqlite3.Error as err:
			print(err)
			raise err

		return

	def add(self, table, data):
		if not self.__verify(table, data):
			print("Bad input")
			raise

		self.connect()
		for k in data.copy():
			if not bool(data[k]):
				del data[k]

		_keys, _values = data.keys(), data.values()
		keys, values = ", ".join(_keys), "\', \'".join(_values)

		try:
			query = "INSERT INTO {} ({}) VALUES (\'{}\')".format(table, keys, values)
			self.cursor.execute(query)
			self.connection.commit()
			self.lastid = self.cursor.lastrowid
		except sqlite3.Error as err:
			print(err)
			raise

		self.close()
		return

	def update(self, table, data, key, value):
		if not self.__verify(table, data, key, value):
			print("Bad input")
			raise

		self.connect()

		assigments = []
		for index in data.copy():
			if not bool(data[index]):
				data[index] = "NULL"
			assigment = "{}='{}'".format(index, data[index])
			assigments.append(assigment)

		dataset = ",".join(assigments)
		try:
			query = "SELECT * FROM {} WHERE {}=\'{}\'".format(table, key, value)
			self.cursor.execute(query)
			result = self.cursor.fetchone()

			if result:
				query = "UPDATE {} SET {} WHERE {}=\'{}\'".format(table, dataset, key, value)
				self.cursor.execute(query)
				self.connection.commit()
				return

			err = "Not found any row with column '{}' equal to '{}' in '{}' table.".format(key, value, table)
			raise sqlite3.Error(err)
		except sqlite3.Error as err:
			print("Bad input")
			raise

		self.close()
		return

	def delete(self, table, data):
		if not self.__verify(table, data):
			print("Bad input")
			raise

		self.connect()

		filters = []
		for k in data.copy():
			if not bool(data[k]):
				del data[k]
			else:
				filters.append("{}=\'{}\'".format(k, data[k]))

		filter = " AND ".join(filters)
		query = "DELETE FROM {} WHERE {}".format(table, filter)
		try:
			self.cursor.execute(query)
			self.connection.commit()
		except sqlite3.Error as err:
			print(err)
			raise

		self.close()
		return

	def get(self, table, filters):
		if not self.__verify(table, filters):
			print("Bad input")
			raise

		constrains = []
		for index in filters:
			constrains.append("{}=\'{}\'".format(index, filters[index]))

		where = " AND ".join(constrains)
		query, result = "SELECT * FROM {} WHERE {}".format(table, where), {}

		self.connect()
		try:
			self.cursor.execute(query)
			result = self.cursor.fetchone()
		except sqlite3.Error as err:
			print(err)
			raise

		self.close()
		return result

	def getAll(self, table, key=None, value=None):
		if not self.__verify(table):
			print("Bad input")
			raise

		self.connect()
		query, results = "SELECT * FROM %s" % table, []

		if key:
			if not value:
				print("Bad input")
				raise

			query = "%s WHERE %s=\'%s\'" % (query, key, value)

		try:
			self.cursor.execute(query)
			results = self.cursor.fetchall()
		except sqlite3.Error as err:
			print(err)
			raise

		self.close()
		return results

	def search(self, table, key=None, value=None):
		if not self.__verify(table):
			print("Bad input")
			raise

		self.connect()
		query, results = "SELECT * FROM %s" % table, []

		if key:
			if not value:
				print("Bad input")
				raise

		try:
			q = "{q} WHERE {k} LIKE \'{v}%\'".format(q=query, k=key, v=value)
			self.cursor.execute(q)
			results = self.cursor.fetchall()

			q = "{q} WHERE {k} LIKE \'% {v}%\'".format(q=query, k=key, v=value)
			self.cursor.execute(q)
			results = results + self.cursor.fetchall()
		except sqlite3.Error as err:
			print(err)
			raise

		self.close()
		return results

	def count(self, table, key, value):
		if not self.__verify(table, key, value):
			print("Bad input")
			raise

		self.connect()
		query, result = "SELECT COUNT(*) FROM %s WHERE %s=\'%s\'" % (table, key, value), 0

		try:
			self.cursor.execute(query)
			row_result = self.cursor.fetchone()
			result = row_result.itervalues().next()
		except sqlite3.Error as err:
			print(err)
			raise

		self.close()
		return result

	def close(self):
		try:
			self.connection.close()
		except sqlite3.Error as err:
			print(err)
			raise

		return