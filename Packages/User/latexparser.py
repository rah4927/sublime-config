# Token Object (token, type of token)
class Token: 
	def __init__(self, token, token_type):
		self.token = token 
		self.token_type = token_type

	
	def set_type(self, token_type):
		self.token_type = token_type 

class LatexParser: 
	# transition characters
	BACKSLASH = '\\'
	COLON = ':'
	EXPONENT = '^'
	SUBSCRIPT = '_'
	LEFT_BRACKET = '{'
	RIGHT_BRACKET = '}'
	LEFT_PAREN = '('
	RIGHT_PAREN = ')'
	LEFT_SQUARE = '['
	RIGHT_SQUARE = ']'
	SPACE = ' '

	# self.states 
	SLASH = "SLASH"
	OPERATION = "OP"
	ARGUMENT = "ARG"
	NEU = "NEU"
	SUBEXP = "SUBEXP"

	def __init__(self, string):
		self.string = string 
		# global variables 
		self.command = ""
		self.state = LatexParser.NEU 

		#list of tokens 
		self.token_list = []

		# paired parenthesis 
		self.pair_paren = 0 

	def backslash(self, char):
		 
		if self.state == LatexParser.NEU: 
			if ((not self.command.isspace()) and self.command != ""): 
				newToken = Token(self.command, self.state) #end prevToken
				self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.SLASH #change self.state 
			self.command = "" #create new token 

		elif self.state == LatexParser.OPERATION: 
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list
			self.state = LatexParser.SLASH #change self.state 
			self.command = "" #create new token 
			
		elif self.state == LatexParser.ARGUMENT: 
			self.command += char # update token 

		elif self.state == LatexParser.SUBEXP: 
			pass #do nothing, impossible case 

		return 
	

	def colon(self, char): 
		 

		if self.state == LatexParser.NEU: 
			self.command += char 

		elif self.state == LatexParser.OPERATION: 
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.NEU #change self.state 
			self.command = ":" #create new token 

		elif self.state == LatexParser.SLASH: 
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.NEU #change self.state 
			self.command = ":" #create new token  

		elif self.state == LatexParser.ARGUMENT: 
			self.command += char 

		elif self.state == LatexParser.SUBEXP: 
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.NEU #change self.state 
			self.command = ":" #create new token

		return  

	def exponent(self, char): 
		 
		if self.state == LatexParser.NEU:
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.SUBEXP #change self.state 
			self.command = "^" #create new token
			newToken = Token(self.command, LatexParser.OPERATION) #end prevToken
			self.token_list.append(newToken) # append token to list
			self.command = "" #create newNewToken

			
		elif self.state == LatexParser.OPERATION: 
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.SUBEXP #change self.state 
			self.command = "^" #create new token
			newToken = Token(self.command, LatexParser.OPERATION) #end prevToken
			self.token_list.append(newToken) # append token to list
			self.command = "" #create newNewToken

		elif self.state == LatexParser.SLASH: 
			pass

		elif self.state == LatexParser.ARGUMENT: 
			self.command += char # update token

		elif self.state == LatexParser.SUBEXP:
			pass # not possible 

		return 

	def subscript(self, char): 
		 
		if self.state == LatexParser.NEU:
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.SUBEXP #change self.state 
			self.command = "_" #create new token
			newToken = Token(self.command, LatexParser.OPERATION) #end prevToken
			self.token_list.append(newToken) # append token to list
			self.command = "" #create newNewToken

			
		elif self.state == LatexParser.OPERATION: 
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.SUBEXP #change self.state 
			self.command = "_" #create new token
			newToken = Token(self.command, LatexParser.OPERATION) #end prevToken
			self.token_list.append(newToken) # append token to list
			self.command = "" #create newNewToken

		elif self.state == LatexParser.SLASH: 
			pass

		elif self.state == LatexParser.ARGUMENT: 
			self.command += char # update token

		elif self.state == LatexParser.SUBEXP:
			pass # not possible 

		return 

	def left_bracket(self, char): 
		 
		if self.state == LatexParser.NEU: 
			if ((not self.command.isspace()) and self.command != ""):
				newToken = Token(self.command, self.state) #end prevToken
				self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.ARGUMENT #change self.state 
			self.command = "" #create new token
			self.pair_paren += 1

		elif self.state == LatexParser.OPERATION: 
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.ARGUMENT #change self.state 
			self.command = "" #create new token
			self.pair_paren += 1

		elif self.state == LatexParser.SLASH:
			self.state = LatexParser.NEU #change self.state 
			self.command = "{" #create new token 

		elif self.state == LatexParser.ARGUMENT: 
			self.command += char # update token
			self.pair_paren += 1 # pair paren 

		elif self.state == LatexParser.SUBEXP:  
			self.state = LatexParser.ARGUMENT #change self.state 
			self.command = "" #create new token
			self.pair_paren += 1

		return 


	def right_bracket(self, char):
		 
		if self.state == LatexParser.NEU: 
			pass # not possible

		elif self.state == LatexParser.OPERATION: 
			pass # not possible 

		elif self.state == LatexParser.SLASH:
			self.state = LatexParser.NEU #change self.state 
			self.command = "}" #create new token 
			
		elif self.state == LatexParser.ARGUMENT: 
			self.pair_paren -= 1 # pair paren

			if self.pair_paren != 0: 
				self.command += char # update token
			elif self.pair_paren == 0: 
				newToken = Token(self.command, self.state) #end prevToken
				self.token_list.append(newToken) # append token to list 
				self.state = LatexParser.NEU #change self.state 
				self.command = "" #create new token

		elif self.state == LatexParser.SUBEXP:
			pass # not possible 

		return 

	def left_paren(self, char): 
		 
		if self.state == LatexParser.NEU: 
			self.command += char # update token
			
		elif self.state == LatexParser.OPERATION: 
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.NEU #change self.state 
			self.command = "(" #create new token

		elif self.state == LatexParser.SLASH: 
			pass
		
		elif self.state == LatexParser.ARGUMENT: 
			self.command += char # update token 

		elif self.state == LatexParser.SUBEXP: 
			pass # not possible

		return 

	def right_paren(self, char): 
		 
		if self.state == LatexParser.NEU: 
			self.command += char # update token

		elif self.state == LatexParser.OPERATION: 
			pass # not possible

		elif self.state == LatexParser.ARGUMENT: 
			self.command += char # update token

		elif self.state == LatexParser.SUBEXP: 
			pass # not possible

		return 

	def left_square(self, char):
		 
		if self.state == LatexParser.NEU: 
			self.command += char # update token
			
		elif self.state == LatexParser.OPERATION: 
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.NEU #change self.state 
			self.command = "[" #create new token
		
		elif self.state == LatexParser.ARGUMENT: 
			self.command += char # update token 

		elif self.state == LatexParser.SLASH: 
			pass

		elif self.state == LatexParser.SUBEXP: 
			pass # not possible

		return 
			

	def right_square(self, char):
		 
		if self.state == LatexParser.NEU: 
			self.command += char # update token

		elif self.state == LatexParser.OPERATION: 
			pass # not possible

		elif self.state == LatexParser.SLASH: 
			pass

		elif self.state == LatexParser.ARGUMENT: 
			self.command += char # update token

		elif self.state == LatexParser.SUBEXP: 
			pass # not possible

		return 

	# This is incorrect right now
	# Confused with the previous function LMAO 
	def space(self, char): 
		 
		if self.state == LatexParser.NEU: 
			self.command += char # update token

		elif self.state == LatexParser.OPERATION: 
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list 
			self.state = LatexParser.NEU #change self.state 
			self.command = "" #create new token

		elif self.state == LatexParser.SLASH: 
			pass

		elif self.state == LatexParser.ARGUMENT: 
			self.command += char # update token

		elif self.state == LatexParser.SUBEXP: 
			pass # not possible

		return 


	def neutral(self, char): 
		 

		if self.state == LatexParser.NEU: 
			self.command += char # update token

		elif self.state == LatexParser.OPERATION: 
			self.command += char # update token

		elif self.state == LatexParser.SLASH:
			self.command += char 
			self.state = LatexParser.OPERATION  

		elif self.state == LatexParser.ARGUMENT: 
			self.command += char # update token

		elif self.state == LatexParser.SUBEXP:
			self.state = LatexParser.ARGUMENT #change self.state 
			self.command = str(char) #create new token 
			newToken = Token(self.command, self.state) #end prevToken
			self.token_list.append(newToken) # append token to list
			self.state = LatexParser.NEU
			self.command = "" 

		return 


	# Optimize this with dictionary 
	def transition(self, char):
		if char ==  LatexParser.BACKSLASH:
			self.backslash(char)

		elif char == LatexParser.COLON:
			self.colon(char)
		
		elif char == LatexParser.EXPONENT:
			self.exponent(char)

		elif char == LatexParser.SUBSCRIPT:
			self.subscript(char)

		elif char == LatexParser.LEFT_BRACKET:
			self.left_bracket(char)

		elif char == LatexParser.RIGHT_BRACKET:
			self.right_bracket(char)

		elif char == LatexParser.LEFT_PAREN:
			self.left_paren(char)

		elif char == LatexParser.RIGHT_PAREN:
			self.right_paren(char)

		elif char == LatexParser.LEFT_SQUARE: 
			self.left_square(char)

		elif char == LatexParser.RIGHT_SQUARE:
			self.right_square(char)

		elif char == LatexParser.SPACE: 
			self.space(char)

		else:
			self.neutral(char)

		return  

	def dfa(self): 
		for char in self.string: 
			self.transition(char) 
		if ((not self.command.isspace()) and self.command != ""): 
				newToken = Token(self.command, self.state) #end prevToken
				self.token_list.append(newToken) # append token to list
		return 

	def printToken(self):
		for item in self.token_list:
				print(item.token + " " + item.token_type)






