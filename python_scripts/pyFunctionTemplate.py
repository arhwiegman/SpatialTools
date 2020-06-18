# buildFunctionDictionary --------------------------
# searches for functions in python script and creates a dicitonary
# all functions must be organized with the same format...
# =================== example format =======================
# (Line 1)      # functionName ---------------
# (Line 2)      # function description 
# (Line 3 to n) # additional links and build notes 
# (Line n+1)    def functionName
# ===========================================================
def buildFunctionDictionary(pyscript=None):
	
	rewind = lambda f: f.seek(0) #function to rewind file 
	import re
	import os 
	if pyscript == None: pyscript = os.path.basename(__file__)
	f = open(pyscript,"r")
	print("reading " + pyscript)
	script = f.read()
	rewind(f)
	print("!!!!!!!!! START OF FILE: "+pyscript+" !!!!!!!!!!!!!")
	print(script)
	print("!!!!!!!!! END OF FILE:   "+pyscript+" !!!!!!!!!!!!!")
	# regular expression search for all functions
	print("searching script for functions...")
	pattern = "#\s(\S+)\s\-+\n#(.*)\n"
	functions = re.findall(pattern,script)
	dictionary = dict()
	# store function name and descriptions as dictionary
	print("building function dictionary...")
	print("...")
	for i in range(len(functions)):
		dictionary[functions[i][0]] = functions[i][1]
	print("FUNCTION DICTIONARY: ")
	print(dictionary)
	return(dictionary)
functionDictionary = buildFunctionDictionary()
print("building function dictionary...")

# functionName ----------------
# function description
# comments and links
def functionName():
	# do something
	return("expression")
# function_Name ----------------
# function description
# comments and links
def functionName():
	# do something
	return("expression")

# functiopoe.nName ----------------
# function description decrsciption
# comments and links
def functionName():
	# do something
	return("expression")