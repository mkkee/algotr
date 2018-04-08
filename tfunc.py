#module to define trading functions
from anytree import Node, RenderTree;
from random import *;
import tfdb;

TF_number_min = 1;
TF_number_max = 300;
TF_functionToNumberPercentage = 80; #70 will generate 70% function and 30% numbers

TF_population_size = 1000;

#name, type, min val, max val
TF_argument_types = [
 ['time', 'int', 1, 10]
,['period', 'int', 1, 10]
];

TF_operators = [
 '+'
,'-'
,'*'
,'/'
];

TF_compare_operators = [
 '<'
,'>'
];

TF_logical_operators = [
 'and'
,'or'
#,'xor'
]

#this is dictionary with info about params
TF_functionList = [
 ['TF_low', 1, 'time']
,["TF_high", 1, 'time']
,["TF_open", 1, 'time']
,["TF_close", 1, 'time']
,["TF_min", 2, 'time', 'period']
,["TF_max", 2, 'time', 'period']
,["TF_avg_open", 2, 'time', 'period']
];


def TF_low(t):
	return tfdb.__TF_DB__[t][5];
	
def TF_high(t):
	return tfdb.__TF_DB__[t][4];

def TF_open(t):
	#print(TF_DB[0]);
	return tfdb.__TF_DB__[t][3];

def TF_close(t):
	return tfdb.__TF_DB__[t][6];
	
def TF_max(t, p):
	m=0;
	for r in tfdb.__TF_DB__[t:t+p]:
			m = max(m, r[4]);
	return m;

def TF_min(t, p):
	m=0;
	for r in tfdb.__TF_DB__[t:t+p]:
		m = min(m, r[5]);
	return m;
	
def TF_avg_open(t, p):
	m=0;
	for r in tfdb.__TF_DB__[t-p+1:t+1]:
		m += r[3];	
	return m/p;
	