import mysql.connector
from mysql.connector import errorcode
from getpass import getpass

def connectSQL():
	# password= getpass("Enter mySQL password: ")
	db_name = 'twitter_info_sql'
	try:
		cnx = mysql.connector.connect(user='noah', password= 'QuakerValley14',
	    	                          host='127.0.0.1',
	        	                      database=db_name)

	except mysql.connector.Error as err:
	  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
	    print("Something is wrong with your username or password")
	  elif err.errno == errorcode.ER_BAD_DB_ERROR:
	    print("Database does not exist")
	  else:
	    print(err)
	return cnx


def createTables(handles):
	db_name = 'twitter_info_sql'
	tables = {}

	for handle in handles:

		tables[handle] = (
		    "CREATE TABLE IF NOT EXISTS `" + handle + "` ("
		    "  `handle` TEXT CHARACTER SET utf8,"
		    "  `entities` TEXT CHARACTER SET utf8,"
		    "  `labels` TEXT CHARACTER SET utf8,"
		    "  `texts` SMALLINT,"
		    "  PRIMARY KEY (`handle`)"
		    ") ENGINE=InnoDB")

	for name, ddl in tables.iteritems():
	    try:
	        print("Creating table {}: ".format(name)),
	        cursor.execute(ddl)
	    except mysql.connector.Error as err:
	        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
	            print("already exists.")
	        else:
	            print(err.msg)
	    else:
	        print("OK")

def insertEx(cursor, cnx):
	db_name = 'twitter_info_sql'
	tables = {}
	date = "0408"
	tables[date] = (
	    "CREATE TABLE IF NOT EXISTS `" + date + "` ("
	    "  `date` TEXT CHARACTER SET utf8,"
	    "  `handle` varchar(40) NOT NULL,"
	    "  `entities` TEXT CHARACTER SET utf8,"
	    "  `labels` TEXT CHARACTER SET utf8,"
	    "  `texts` SMALLINT,"
	    "  PRIMARY KEY (`date`)"
	    ") ENGINE=InnoDB")

	for name, ddl in tables.iteritems():
	    try:
	        print("Creating table {}: ".format(name)),
	        cursor.execute(ddl)
	    except mysql.connector.Error as err:
	        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
	            print("already exists.")
	        else:
	            print(err.msg)
	    else:
	        print("OK")

	name = "Some new city"
 
	country_code = 'SNC'
	 
	district = 'Someyork'
	 
	population = 10008
	 
	data = [
	('city 1', 'MAC', 'distrct 1', 16822),
	('city 2', 'PSE', 'distrct 2', 15642),
	('city 3', 'ZWE', 'distrct 3', 11642),
	('city 4', 'USA', 'distrct 4', 14612),
	('city 5', 'RPD', 'distrct 5', 17672),
	]
	 
	sql = "insert into city(date, handle, entities, texts) VALUES(%s, %s, %s, %s)"
	 
	number_of_rows = cursor.executemany(sql, data)
	cnx.commit()
	'''
	sql = "insert into 4/8(date, handle, entities, labels, texts) VALUES(%s, %s, %s, %s, %s)"
	execdata = [('4/8', 'justinbieber', 'entity thing', 'label thing', 'text thing')]
	cursor.executemany(sql, execdata)
	cnx.commit()
	'''

def main():
	handles = ['katyperry', 'justinbieber', 'BarackObama', 'YouTube', 'Cristiano', 'jtimberlake', 'NeilTyson', 'BillNye', 'ElonMusk', 'cnnbrk',
	'BillGates', 'Oprah', 'BrunoMars', 'Drake', 'espn', 'MileyCyrus', 'KevinHart4real', 'instagram', 'taylorswift13', 'ladygaga']
	cnx = connectSQL()
	cursor = cnx.cursor()
	insertEx(cursor, cnx)
	cursor.close()
	cnx.close()
   
 
if __name__ == '__main__':
    main()