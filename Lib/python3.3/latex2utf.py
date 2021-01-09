from latexparser import * 
import json 
from substitutions import *

num_args = 'num args'
mapsto = 'mapsto'
NaN = 'NaN'

def jsonToDict(filename): 
	mydict = json.load( open( filename + ".json" ) )
	return mydict

# substitutions = jsonToDict("LateX substitutions")


def latex2utf(command): 
	parser = LatexParser(command)
	parser.dfa() 

	utf = ""
	t_list = parser.token_list
	i = 0 
	while i < len(t_list): 
		token = t_list[i]
		if 	token.token_type == LatexParser.OPERATION: 
			item = substitutions.get(token.token, 0)
			try: 
				if item != 0:
					num = item[num_args]
					if num == 1:
						arg = t_list[i + 1].token
						utf = utf + item[mapsto][arg]
						i = i + 2
					elif num == 0: 
						utf = utf + item[mapsto][NaN]
						i = i + 1
				else: 
					utf = utf + token.token 
					i = i + 1 
			
			except: 
				utf = utf + token.token 
				i = i + 1 
		else: 
			utf = utf + token.token
			i = i + 1
	
	return utf 

