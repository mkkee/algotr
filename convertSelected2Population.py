import csv;
from timeit import default_timer as timer
import sys;
from glob import glob;
	
##############################################################################################################	
start_time = timer()

print("Started");
print('Argument List:', str(sys.argv))

#file_name = sys.argv[1];
error_cnt=0;
cnt = 0;

#file format is: ("Result | Result per Trans | Trans Cnt | Signal Type | Strategy Type | Positive Trans Cnt | Positive Trans Pct | Eq in Str | JSON | Transaction Map");
print("############################################################### DATA TO FOLLOW ########################################");	
for file_name in glob(sys.argv[1]):
	with open(file_name, newline='') as csvfile:
		filereader = csv.reader(csvfile, delimiter = '|');
		for row in filereader:
			cnt = cnt + 1;
			try:
				data_signal_type  = row[3];
				data_json = row[8];
				#print(data_signal_type);
				if data_signal_type == 'True':
					data_true_cnt = 0;
					data_false_cnt = 1;
				else:
					data_true_cnt = 1;
					data_false_cnt = 0;
				print(str(data_true_cnt)+"|"+str(data_false_cnt)+"|0|0|0|"+data_json);
	#output is: ("True count | False count | Found # | Equation # | Found Pct | Json");	
			except: #skipping wrong rows
				1==1;
				error_cnt = error_cnt + 1;
				continue;

print("############################################################### DATA END ##############################################");	

print("Converted population data. Count =", cnt, "with ", error_cnt, "errors");

print("End");
end_time = timer();
print("Elapsed Time: ", end_time - start_time);

exit(0);