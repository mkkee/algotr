import tfdb;
from tfunc import *;

from random import *;
from anytree import Node, RenderTree;


def TF_getArgumentValue(p):
#	seed();
	param = "";
	v = 0;
	for i in TF_argument_types:
		if i[0] == p:
			param = i;
			break;
	#print(param);
	param_type = param[1];
	param_min = param[2];
	param_max = param[3];
	
	if param_type == 'int':	
		v = randrange(param_min, param_max + 1);
	
	return v;
	
	
def TF_genFunctionStatement():
	params = [];
#	seed();
	f = choice(TF_functionList);
	f_name = f[0];
	f_param_num = f[1];
	#print(f_name, f_param_num, f);
	f_statement = f_name + "(";
	#do all params for the func
	comma = '';
	for i in range(f_param_num):
		f_statement = f_statement + comma + str(TF_getArgumentValue(f[i+2]));
		comma = ',';		
	f_statement = f_statement + ")";
	return f_statement;

def TF_genEquationElement():
	#decide if this is function or number
	if randrange(0, 101) <= TF_functionToNumberPercentage:
		#function
		return TF_genFunctionStatement();
	else:
		return str(randrange(TF_number_min, TF_number_max+1));
		#number

#gets equation element in a form of XXX > YYY or XXX < YYY [func|num][compare_op][func|num] in brackets		
def TF_genEquationElementCompare():
	stmt = "(";
	#decide if this is function or number
	if randrange(0, 101) <= TF_functionToNumberPercentage:
		#function
		stmt = stmt + TF_genFunctionStatement();
	else:
		stmt = stmt + str(randrange(TF_number_min, TF_number_max+1));
		#number
	stmt = stmt + " " + TF_genEquationOperatorCompare() + " ";
	if randrange(0, 101) <= TF_functionToNumberPercentage:
		#function
		stmt = stmt + TF_genFunctionStatement();
	else:
		stmt = stmt + str(randrange(TF_number_min, TF_number_max+1));
		#number
	stmt = stmt + ")";
	return stmt;
		
def TF_genEquationOperator():
	return TF_operators[randrange(0, len(TF_operators))];

def TF_genEquationOperatorCompare():
	return TF_compare_operators[randrange(0, len(TF_compare_operators))];
	
def TF_genEquationOperatorLogical():
	return TF_logical_operators[randrange(0, len(TF_logical_operators))];

def TF_genEquationAlgTree(iterations=0):
	o = Node(TF_genEquationOperator());	
	l = Node(TF_genEquationElement());
	r = Node(TF_genEquationElement());
	t = o;	
	t.children = [l, r];
	#randomize number of iterations
	iter = randrange(iterations);
	for i in range(iter):
		o = Node(TF_genEquationOperator());	
		l = Node(TF_genEquationElement());
		r = Node(TF_genEquationElement());
		#move descendants that are leafs to table for randomization
		d = [];
		for desc in t.descendants:
			if desc.is_leaf:
				d.append(desc);
		#choose randomly which descendant to modify
		n = d[randrange(len(d))];
		#print(t.descendants);
		n.name = o.name;
		n.children = [l, r];
	return t;

def TF_genEquationAlgTreeLogical(iterations=0):
	o = Node(TF_genEquationOperatorLogical());	
	l = Node(TF_genEquationElementCompare());
	r = Node(TF_genEquationElementCompare());
	t = o;	
	t.children = [l, r];
	#randomize number of iterations
	iter = randrange(iterations);
	for i in range(iter):
		o = Node(TF_genEquationOperatorLogical());	
		l = Node(TF_genEquationElementCompare());
		r = Node(TF_genEquationElementCompare());
		#move descendants that are leafs to table for randomization
		d = [];
		for desc in t.descendants:
			if desc.is_leaf:
				d.append(desc);
		#choose randomly which descendant to modify
		n = d[randrange(len(d))];
		#print(t.descendants);
		n.name = o.name;
		n.children = [l, r];
	return t;
	
def TF_getTreeAsString(t):
	s = "";	
	c = t.children;
	if c[0].is_leaf:
		s += '('+c[0].name#+c[0].parent.name;
	else:
		#1==1;
		s += '('+TF_getTreeAsString(c[0]);
	
	s += c[0].parent.name;
	
	if c[1].is_leaf:
		s += c[1].name+')' #+ c[1].parent.name;
	else:
		#1==1;
		s += TF_getTreeAsString(c[1]) + ')';
		
	return s;

