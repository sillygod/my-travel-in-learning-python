'''
	input: sql query
	output: sql token, data type double list
'''
import re

class sqlAnalyzer:
	''' 
		the analyze the sql query and split it into three part 
		1. attribute list
		2. table list 
		3. condition list 
		
		addition: need to do basic syntax check  
	'''
	def __init__(self, sqlQuery):
		self.msqlQuery = sqlQuery.upper() # due to non support for case sensitive, so all are compelled to transfer to capital
		self.attributeList = []
		self.tableList = []
		self.conditionList = []

	# using reverse is for the conveninet of parser
	def getAttribList(self):
		return self.attributeList
	
	def getTableList(self):
		return self.tableList
		
	def getConditionList(self):
		return self.conditionList

	def startAnalyze(self):
		''' output a list of attribute '''
		attributeString, mid, rhs = self.msqlQuery.partition('SELECT')[2].partition('FROM') # the part of attribute 
		tableString, mid, rhs = rhs.partition('WHERE') # the part of table list
		
		self.attributeList.append( re.split('[\s\(\),]+',attributeString) )
		self.tableList.append( re.split('[\s\(\),]+',tableString) )
		
		#need to check whether it is a nested sql or not
		if rhs.partition('SELECT')[1] == '':
			conditionString = rhs
			self.conditionList.append( re.split('[\s\(\),]+', conditionString) )

			self.attributeList.reverse()
			self.tableList.reverse()
			self.conditionList.reverse()
		else:
			self.conditionList.append( re.split('[\s\(\),]+', rhs.partition('SELECT')[0]) )
			self.msqlQuery=rhs.partition('SELECT')[1]+rhs.partition('SELECT')[2]
			self.startAnalyze()