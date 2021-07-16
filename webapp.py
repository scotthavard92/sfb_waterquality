import sqlite3
from flask import g
from flask import Flask
from flask import render_template

DATABASE = '/Users/scotthavard/desktop/sfb_waterquality/db.db'

class location_data_point:
    def __init__(self, station_code, sample_date, analyte, result, unit): 
	    self.station_code = station_code 
	    self.sample_date = sample_date
	    self.analyte = analyte
	    self.result = result
	    self.unit = unit

app = Flask(__name__)

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

def get_alameda_enterococcus_data():
	sql = '''SELECT DISTINCT * FROM alameda WHERE analyte LIKE "Enterococcus" ORDER BY sample_date DESC LIMIT 1; '''
	result = query_db(sql)
	data = result[0]

	ret_object = location_data_point(data[1], data[2], data[3], data[4], data[5])

	return ret_object

def get_alameda_coliform_total_data():
	sql = '''SELECT DISTINCT * FROM alameda WHERE analyte LIKE "Coliform, Total" ORDER BY sample_date DESC LIMIT 1; '''
	result = query_db(sql)
	data = result[0]

	ret_object = location_data_point(data[1], data[2], data[3], data[4], data[5])

	return ret_object

def get_alameda_coliform_total_data():
	sql = '''SELECT DISTINCT * FROM alameda WHERE analyte LIKE "Coliform, Total" ORDER BY sample_date DESC LIMIT 1; '''
	result = query_db(sql)
	data = result[0]

	ret_object = location_data_point(data[1], data[2], data[3], data[4], data[5])

	return ret_object

def get_alameda_coliform_fecal_data():
	sql = '''SELECT DISTINCT * FROM alameda WHERE analyte LIKE "Coliform, Fecal" ORDER BY sample_date DESC LIMIT 1; '''
	result = query_db(sql)
	data = result[0]

	ret_object = location_data_point(data[1], data[2], data[3], data[4], data[5])

	return ret_object

def get_ap_coliform_total_data():
	sql = '''SELECT DISTINCT * FROM aquatic_park_sf WHERE analyte LIKE "Coliform, Total" ORDER BY sample_date DESC LIMIT 1; '''
	result = query_db(sql)
	data = result[0]

	ret_object = location_data_point(data[1], data[2], data[3], data[4], data[5])

	return ret_object

def get_ap_enterococcus_data():
	sql = '''SELECT DISTINCT * FROM aquatic_park_sf WHERE analyte LIKE "Enterococcus" ORDER BY sample_date DESC LIMIT 1; '''
	result = query_db(sql)
	data = result[0]

	ret_object = location_data_point(data[1], data[2], data[3], data[4], data[5])

	return ret_object

def get_ap_ecoli_data():
	sql = '''SELECT DISTINCT * FROM aquatic_park_sf WHERE analyte LIKE "E. Coli" ORDER BY sample_date DESC LIMIT 1; '''
	result = query_db(sql)
	data = result[0]

	ret_object = location_data_point(data[1], data[2], data[3], data[4], data[5])

	return ret_object

def clean_string_data(result_string):
	result_string_v = str(result_string)
	cleaned = result_string_v.split(" ", 1)[0]

	return int(cleaned)

def check_ent_safety(result_object_val):
	value = clean_string_data(result_object_val)

	if (value > 60):
		return False

	return True

def check_ecoli_safety(result_object_val):
	value = clean_string_data(result_object_val)

	if (value > 190):
		return False

	return True

@app.route("/")
def run_app():
	alameda_safe = False
	sf_aquatic_park_safe = False

	alameda_ent_obj = get_alameda_enterococcus_data()
	alameda_col_tot_obj = get_alameda_coliform_total_data()
	alameda_col_fec_obj = get_alameda_coliform_fecal_data()

	ap_ent_obj = get_ap_enterococcus_data()
	ap_col_tot_obj = get_ap_coliform_total_data()
	ap_ecoli_obj = get_ap_ecoli_data()

	alameda_safe = check_ent_safety(alameda_ent_obj.result)
	if (check_ent_safety(ap_ent_obj.result) and check_ecoli_safety(ap_ecoli_obj.result)):
		sf_aquatic_park_safe = True

	return render_template('homepage.html',\
	al_ent_stat_code=alameda_ent_obj.station_code,\
	al_ent_sample_date=alameda_ent_obj.sample_date,\
	al_ent_analyte=alameda_ent_obj.analyte,\
	al_ent_result=alameda_ent_obj.result,\
	al_ent_unit=alameda_ent_obj.unit,\
	al_col_t_stat_code=alameda_col_tot_obj.station_code,\
	al_col_t_sample_date=alameda_col_tot_obj.sample_date,\
	al_col_t_analyte=alameda_col_tot_obj.analyte,\
	al_col_t_result=alameda_col_tot_obj.result,\
	al_col_t_unit=alameda_col_tot_obj.unit,\
	al_col_f_stat_code=alameda_col_fec_obj.station_code,\
	al_col_f_sample_date=alameda_col_fec_obj.sample_date,\
	al_col_f_analyte=alameda_col_fec_obj.analyte,\
	al_col_f_result=alameda_col_fec_obj.result,\
	al_col_f_unit=alameda_col_fec_obj.unit,\
	ap_col_t_stat_code=ap_col_tot_obj.station_code,\
	ap_col_t_sample_date=ap_col_tot_obj.sample_date,\
	ap_col_t_analyte=ap_col_tot_obj.analyte,\
	ap_col_t_result=ap_col_tot_obj.result,\
	ap_col_t_unit=ap_col_tot_obj.unit,\
	ap_ent_stat_code=ap_col_tot_obj.station_code,\
	ap_ent_sample_date=ap_ent_obj.sample_date,\
	ap_ent_analyte=ap_ent_obj.analyte,\
	ap_ent_result=ap_ent_obj.result,\
	ap_ent_unit=ap_ent_obj.unit,\
	ap_ecoli_stat_code=ap_col_tot_obj.station_code,\
	ap_ecoli_sample_date=ap_ecoli_obj.sample_date,\
	ap_ecoli_analyte=ap_ecoli_obj.analyte,\
	ap_ecoli_result=ap_ecoli_obj.result,\
	ap_ecoli_unit=ap_ecoli_obj.unit,\
	sf_aquatic_park_safe=sf_aquatic_park_safe,\
	alameda_safe=alameda_safe)

