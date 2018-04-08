import csv;

global __TF_DB__;

__TF_DB__ = [];

def TF_DBLoad():
	with open('gbpjpy.txt', newline='') as csvfile:
		filereader = csv.reader(csvfile, delimiter = ',');
		filereader.__next__(); #skip first line
		for row in filereader:
			data_date = row[0];
			data_time = row[1];
			data_open = float(row[2]);
			data_high = float(row[3]);
			data_low = float(row[4]);
			data_close = float(row[5]);
			db_row = ['GBPJPY', data_date, data_time, data_open, data_high, data_low, data_close];
			__TF_DB__.append(db_row);

	__TF_DB__.reverse();
	

