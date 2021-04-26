#!/bin/python
#
# This file was made by ebalo, contact at:
# webdev [dot] ebalo [at] gmail [dot] com
#
# INSTALLATION
# python3 -m pip install mysql-connector-python

from mysql.connector import connect, Error

class WordExtractor:
	"""
	Word extractor class used to extract words and their associated meaning 
	from a mysql / mariadb database, tested on the latest mariadb version
	"""
	def __init__(self, host, user, psw, db):
		"""
		 Initialize the connection to the backend database, it uses the mysql
		 connector for python, this perfectly works with mariadb if mysql version is
		 below 8.
		 
		 required parameters:
		 	- host: The host where the database is located,
		 	- user: Username to login to the database service
		 	- psw: Password associated to the username
		 	- db: Database (name) to connect to
		 	- port: undefined in the class constructor, defaults to 3306
		"""
		try:
			with connect(
				host=host,
				user=user,
				password=psw,
				database=db
				) as connection:
				# set the class connection instance
				self.connection = connection
		except Error as e:
			# Prints the error end exits
			print(e)
			exit(1)
	
	def _runner(self, query, parameters):
		"""
		PRIVATE METHOD, DO NOT RUN DIRECTLY
		
		Restart the connection to the backend database as that may be closed,
		then runs the query using prepared statements and return the result.
		
		This is a generator function, data are pushed back on the output queue as
		they are retrieved
		"""
		self.connection.reconnect()
		try:
			with self.connection.cursor() as cursor:
				cursor.execute(query, parameters)
				for result in cursor.fetchall():
					yield result
		except Error as e:
			print(e)
			exit(1)
	
	def getWord(self, word):
		query = "SELECT `ScritturaGenerale`.`Parola_fk` FROM `ScritturaGenerale` WHERE `ScritturaGenerale`.`ScritturaGenerale` = %s"
		return self._runner(query, (word,))
	
	def getDescriptions(self, word):
		query = "SELECT * FROM `Parola` INNER JOIN `Descrizione` ON `Parola`.`Parola_pk` = `Descrizione`.`Parola_fk` where `Parola`.`Parola_pk` = %s"
		return self._runner(query, (word,))
	
	def getWordLanguages(self, word):
		query = "SELECT `Lingua` FROM `Parola` WHERE `Parola_pk` = %s"
		return self._runner(query, (word,))
			
	def getExamples(self, word):
		query = "SELECT `Esempio`,`LinguaEsempio` FROM `Esempi` WHERE `Parola_fk` = %s"
		return self._runner(query, (word,))
		
	def getSynonyms(self, word):
		query = "SELECT `Lingua` FROM `Parola` WHERE `Parola_pk` = %s"
		return self._runner(query, (word,))
		
	def getSynonyms(self, word):
		query = "SELECT `Sinonimi(P-P)`.`SI_ParolaB_fk` FROM `Sinonimi(P-P)` WHERE `SI_ParolaA_fk` = %s UNION SELECT `Sinonimi(P-P)`.`SI_ParolaA_fk` FROM `Sinonimi(P-P)` WHERE `SI_ParolaB_fk` = %s"
		return self._runner(query, (word, word,))
		
	def getTranslations(self, word, lang):
		query = ""
		if lang == "IT":
			query = "SELECT `Traduzione(P-P)`.`TR_ParolaIT_fk` FROM `Traduzione(P-P)` WHERE `TR_ParolaEN_fk` = %s"
		else:
			query = "SELECT `Traduzione(P-P)`.`TR_ParolaEN_fk` FROM `Traduzione(P-P)` WHERE `TR_ParolaIT_fk` = %s"
		return self._runner(query, (word,))


# Example usage
#we = WordExtractor("localhost", "root", "palaqwe123", "DBTMM")
#print("Stampa: \n")
#for elem in we.getWord("test"):
	#Elem is a tuple containing all the columns queried
#	print(elem)

