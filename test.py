import json
import requests
import csv
import sqlite3
from sqlite3 import Error

#Cal Gov deprecated old DB
# url_alameda = 'https://data.ca.gov/api/3/action/datastore_search?resource_id=442a2628-92bd-4d83-aab6-6fde5eeeb56c&limit=500&q=alameda'
# url_aquatic_park_sf = 'https://data.ca.gov/api/3/action/datastore_search?resource_id=442a2628-92bd-4d83-aab6-6fde5eeeb56c&limit=500&q=aquatic+park'
# url_ocean_beach_18 = 'https://data.ca.gov/api/3/action/datastore_search?resource_id=442a2628-92bd-4d83-aab6-6fde5eeeb56c&limit=500&q=ocean+beach+san+francisco+18'

#New DB
url_alameda = 'https://data.ca.gov/api/3/action/datastore_search?resource_id=1987c159-ce07-47c6-8d4f-4483db6e6460&limit=500&q=alameda'
url_aquatic_park_sf = 'https://data.ca.gov/api/3/action/datastore_search?resource_id=1987c159-ce07-47c6-8d4f-4483db6e6460&limit=500&q=aquatic+park'
url_ocean_beach_18 = 'https://data.ca.gov/api/3/action/datastore_search?resource_id=1987c159-ce07-47c6-8d4f-4483db6e6460&limit=500&q=ocean+beach+san+francisco+18'

filename = 'water_output_alameda.csv'

# local database
# database = '/Users/scotthavard/desktop/sfswiminfo/sfb_waterquality/db.db'

#hosting database
database = '/home/scotthavard92/sf_swim/sfb_waterquality/db.db'

# Crown 2001 Shoreline Dr.	
# Aquatic Park  
# CHINA CAMP
# MB11 -> San Leandro bay
# Keller North Beach

class location_data_point:
    def __init__(self, station_code, sample_date, analyte, result, unit): 
	    self.station_code = station_code 
	    self.sample_date = sample_date
	    self.analyte = analyte
	    self.result = result
	    self.unit = unit

def read_dataset(url, station_code):
	data_points = []

	while url:
		response = requests.get(url)
		data = response.json()
		result = data['result']
		records = result['records']

		for rec in records:
			if rec['StationCode'] == station_code:
				station_code = rec['StationCode']
				sample_date = rec['SampleDate']
				analyte = rec['Analyte']
				result = rec['Result']
				unit = rec['Unit']

				lcp = location_data_point(station_code, sample_date, analyte, result, unit)
				data_points.append(lcp)
		
		result = data['result']
		links = result['_links']
		url_next = links['next']

		if len(result['records']) != 0:
			url = 'https://data.ca.gov' + url_next
		else:
			url = None
			return data_points
		print(url)

def write_csv(filename, objects):
	with open(filename, 'w') as csvfile:
		fieldnames = ['id', 'station_code', 'sample_date', 'analyte', 'result', 'unit']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		
		dp_id = 1
		writer.writeheader()
		for obj in objects:
			writer.writerow({'id' : dp_id, 'station_code' : obj.station_code, 'sample_date' : obj.sample_date, 'analyte': obj.analyte, 'result': obj.result, 'unit': obj.unit})
			dp_id = dp_id + 1

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table(table_name, connection):
	sql ='''CREATE TABLE IF NOT EXISTS {} (
		id integer PRIMARY KEY,
		station_code text,
		sample_date text,
		analyte text,
		result numeric,
		unit text
		); '''.format(table_name)
	cur = connection.cursor()
	cur.execute(sql)
	connection.commit()


def update_sql_table(objects, table_name, connection):
	with connection:
		dp_id = 1
		for obj in objects:
			station_code = obj.station_code
			sample_date = obj.sample_date
			analyte = obj.analyte
			result = obj.result
			unit = obj.unit
			insert = (dp_id, station_code, sample_date, analyte, result, unit)

			write_row(connection, table_name, insert)
			dp_id = dp_id + 1

def write_row(connection, table_name, object):
    sql = ''' INSERT INTO {}(id, station_code, sample_date, analyte, result, unit)
          VALUES(?,?,?,?,?,?) '''.format(table_name)
    cur = connection.cursor()
    cur.execute(sql, object)
    connection.commit()
    return cur.lastrowid

def delete_table(connetion, table_name):
	sql = "DROP TABLE IF EXISTS {}".format(table_name)
	try:
		cur = connection.cursor()
		cur.execute(sql)
		connection.commit()
	except:
		print("no table exists")

### Run
#Alameda
connection = create_connection(database)
delete_table(connection, "alameda")
dataset = read_dataset(url_alameda, "Crown 2001 Shoreline Dr.")
create_table("alameda", connection)
update_sql_table(dataset, "alameda", connection)
# write_csv(filename, dataset)

#SF Aquatic Park
# connection = create_connection(database)
delete_table(connection, "aquatic_park_sf")
dataset = read_dataset(url_aquatic_park_sf, "Aquatic Park")
create_table("aquatic_park_sf", connection)
update_sql_table(dataset, "aquatic_park_sf", connection)

#SF Ocean Beach
# connection = create_connection(database)
delete_table(connection, "ocean_beach_sf_18")
dataset = read_dataset(url_ocean_beach_18, "OCEAN#18_SL")
create_table("ocean_beach_sf_18", connection)
update_sql_table(dataset, "ocean_beach_sf_18", connection)