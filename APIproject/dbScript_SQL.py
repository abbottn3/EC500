import mysql.connector
import json
from pprint import pprint
from mysql.connector import errorcode
from getpass import getpass
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def connectSQL():
	# password= getpass("Enter mySQL password: ")
	db_name = 'airportInfo'
	try:
		cnx = mysql.connector.connect(user='noah', password= getpass("Enter mySQL password: "),
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


def getAirports(cnx, cursor):
	with open('airports.json') as data_file:
		apdata = json.load(data_file)

	tables = {}
	for airport in apdata:
		code = airport["code"]
		tables[code] = (
	    "CREATE TABLE IF NOT EXISTS `" + code + "` ("
	    "  `city` TEXT CHARACTER SET utf8,"
	    "  `code` VARCHAR(3),"
	    "  `country` TEXT CHARACTER SET utf8,"
	    "  `direct_flights` TEXT CHARACTER SET utf8,"
	    "  `elev` TEXT CHARACTER SET utf8,"
	    "  `email` TEXT CHARACTER SET utf8,"
	    "  `icao` TEXT CHARACTER SET utf8,"
	    "  `lat` TEXT CHARACTER SET utf8,"
	    "  `lon` TEXT CHARACTER SET utf8,"
	    "  `name` TEXT CHARACTER SET utf8,"
	    "  `phone` TEXT CHARACTER SET utf8,"
	    "  `runway_length` TEXT CHARACTER SET utf8,"
	    "  `state` TEXT CHARACTER SET utf8,"
	    "  `type` TEXT CHARACTER SET utf8,"
	    "  `tz` TEXT CHARACTER SET utf8,"
	    "  `url` TEXT CHARACTER SET utf8,"
	    "  `woeid` TEXT CHARACTER SET utf8,"
	    "  PRIMARY KEY (`code`)"
	    ") ENGINE=InnoDB")
	for code, ddl in tables.iteritems():
	    try:
	        print("Creating table {}: ".format(code)),
	        cursor.execute(ddl)
	    except mysql.connector.Error as err:
	        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
	            print("already exists.")
	        else:
	            print(err.msg)
	    else:
	        print("OK")
	enterAirportInfo(apdata, cursor, cnx)

def enterAirportInfo(apdata, cursor, cnx):
	for airport in apdata:
		code = airport["code"]
		sql = "insert into " + code + "(city, code, country, direct_flights, elev, email, icao, lat, lon, name, phone, runway_length, state, type, tz, url, woeid) \
				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % \
		(airport["city"], airport["code"], airport["country"], airport["direct_flights"], airport["elev"], airport["email"],
		airport["icao"], airport["lat"], airport["lon"], airport["name"], airport["phone"], airport["runway_length"],
		airport["state"], airport["type"], airport["tz"], airport["url"], airport["woeid"])
		number_of_rows = cursor.execute(sql)
		cnx.commit()


def main():
	cnx = connectSQL()
	cursor = cnx.cursor()
	getAirports(cnx, cursor)
	cursor.close()
	cnx.close()
   
 
if __name__ == '__main__':
    main()