import json
import sqlite3

from datetime import datetime, timedelta
from flask import g
from flask import Flask
from flask import render_template

### Local Testing
# DATABASE = '/Users/scotthavard/desktop/test_flask_app/db.db'

### Hosting Service 
DATABASE = '/home/scotthavard92/sf_swim/sfb_waterquality/db.db'

app = Flask(__name__)

class chart_data_point:
    def __init__(self, x, y): 
	    self.x = x 
	    self.y = y

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def format_result(result):
	res = str(result[0])
	return res

def get_alameda_chart_data():
	sql_fecal_coli = '''SELECT DISTINCT sample_date, result FROM alameda WHERE analyte LIKE "Coliform, Fecal" ORDER BY sample_date DESC LIMIT 5; '''
	result_fc = query_db(sql_fecal_coli)

	fecal_coli_array = format_chart_data(result_fc)

	sql_entero = '''SELECT DISTINCT sample_date, result FROM alameda WHERE analyte LIKE "Enterococcus" ORDER BY sample_date DESC LIMIT 5; '''
	result_entero = query_db(sql_entero)

	entero_array = format_chart_data(result_entero)

	return chart_data_json("alameda_fecal_coli", "alameda_enterococcus", None, fecal_coli_array, entero_array, None, 2), \
		chart_data_object("alameda_fecal_coli", "alameda_enterococcus", None, fecal_coli_array, entero_array, None, 2)	

def get_sf_ap_chart_data():
	sql_total_coli = '''SELECT DISTINCT sample_date, result FROM aquatic_park_sf WHERE analyte LIKE "Coliform, Total" ORDER BY sample_date DESC LIMIT 5; '''
	result_tc = query_db(sql_total_coli)

	total_coli_array = format_chart_data(result_tc)

	sql_entero = '''SELECT DISTINCT sample_date, result FROM aquatic_park_sf WHERE analyte LIKE "Enterococcus" ORDER BY sample_date DESC LIMIT 5; '''
	result_entero = query_db(sql_entero)

	entero_array = format_chart_data(result_entero)

	sql_ecoli = '''SELECT DISTINCT sample_date, result FROM aquatic_park_sf WHERE analyte LIKE "E. Coli" ORDER BY sample_date DESC LIMIT 5; '''
	result_ecoli = query_db(sql_ecoli)

	ecoli_array = format_chart_data(result_ecoli)

	return chart_data_json("ap_total_coli", "ap_enterococcus", "ap_ecoli", total_coli_array, entero_array, ecoli_array, 3), \
		chart_data_object("ap_total_coli", "ap_enterococcus", "ap_ecoli", total_coli_array, entero_array, ecoli_array, 3)

def get_sf_ob_chart_data():
	sql_total_coli = '''SELECT DISTINCT sample_date, result FROM ocean_beach_sf_18 WHERE analyte LIKE "Coliform, Total" ORDER BY sample_date DESC LIMIT 5; '''
	result_tc = query_db(sql_total_coli)

	total_coli_array = format_chart_data(result_tc)

	sql_entero = '''SELECT DISTINCT sample_date, result FROM ocean_beach_sf_18 WHERE analyte LIKE "Enterococcus" ORDER BY sample_date DESC LIMIT 5; '''
	result_entero = query_db(sql_entero)

	entero_array = format_chart_data(result_entero)

	return chart_data_json("ob_total_coli", "ob_enterococcus", None, total_coli_array, entero_array, None, 2), \
		chart_data_object("ob_total_coli", "ob_enterococcus", None, total_coli_array, entero_array, None, 2)	

def format_chart_data(query_results):
	data_points = []
	for r in query_results:
		data_object = chart_data_point(r[0].replace("T00:00:00", ""), r[1])
		data_points.append(data_object.__dict__)

	return_array = reverse_array(data_points)

	return return_array

def chart_data_object(key1, key2, key3, array1, array2, array3, bact_num):
	if bact_num == 3:
		ret_object = {key1 : array1, key2 : array2, key3 : array3}
	elif bact_num == 2:
		ret_object = {key1 : array1, key2 : array2}
	else:
		ret_object = None
	
	return ret_object

def chart_data_json(key1, key2, key3, array1, array2, array3, bact_num):
	if bact_num == 3: 
		ret_object = {key1 : array1, key2 : array2, key3 : array3}
		ret_json = json.dumps(ret_object, ensure_ascii=False)
	elif bact_num == 2:
		ret_object = {key1 : array1, key2 : array2}
		ret_json = json.dumps(ret_object, ensure_ascii=False)
	else:
		ret_json = None
	

	return ret_json

def reverse_array(array):
	reversed_array = array[::-1]
	return reversed_array

def min_max_date(chart_obj):
	dates = []

	for item in chart_obj.values():
		for obj in item:
			for key, value in obj.items():
				if key == 'x':
					dates.append(datetime.strptime(value, '%Y-%m-%d'))				

	min_date = min(dates)
	max_date = max(dates)

	return min_date, max_date

def get_date_range(min_date, max_date):
	dates = []
	delta = max_date - min_date

	for i in range(delta.days + 1):
		day = min_date + timedelta(days=i)
		dates.append(datetime.strftime(day, '%Y-%m-%d'))

	return dates

@app.route("/")
def run_app():
	alameda_chart_json, alameda_chart_object = get_alameda_chart_data()
	alameda_min_date, alameda_max_date = min_max_date(alameda_chart_object)
	alameda_date_range = get_date_range(alameda_min_date, alameda_max_date)

	sf_ap_chart_json, sf_ap_chart_object = get_sf_ap_chart_data()
	sf_ap_min_date, sf_ap_max_date = min_max_date(sf_ap_chart_object)
	sf_ap_date_range = get_date_range(sf_ap_min_date, sf_ap_max_date)

	sf_ob_chart_json, sf_ob_chart_object = get_sf_ob_chart_data()
	sf_ob_min_date, sf_ob_max_date = min_max_date(sf_ob_chart_object)
	sf_ob_date_range = get_date_range(sf_ob_min_date, sf_ob_max_date)

	return render_template('homepage.html',\
	alameda_chart_object=alameda_chart_json,\
	alameda_date_range=alameda_date_range,\
	sf_ap_chart_object=sf_ap_chart_json,\
	sf_ap_date_range=sf_ap_date_range,\
	sf_ob_chart_object=sf_ob_chart_json,\
	sf_ob_date_range=sf_ob_date_range)

if __name__ == '__main__':
    app.run()
