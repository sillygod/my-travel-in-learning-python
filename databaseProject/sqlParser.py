'''
	This file is for parse the sql query.
	
	basically,
	
	SELECT attribute list 
		*: means to retrieve all the attribute of selected tuples
		DISTINCT: means no duplicate values 
		aggregate function: COUNT, SUM, MIN, AVG , usually combine with GROUP BY
		
		
	FROM table list
	
	WHERE condition 
		default TRUE -- means I don't need to write WHERE TRUE, just write SELECT....FROM...
		AND...AND...AND basic 
		OR bonus
		
	Note:
		1. support for table list name's alias ex. FROM EMPLOYEE E S,  E and S are the alias
		   for the EMPLOYEE
		   
		2. nested sql query IN NOT IN
		3. aggregate function 
		4. no case sensitive, all are capital
		5. GROUP BY, HAVING are the bonus part

	Join condition use equal join?

	remember copy before append a list in some situation
'''

import re
import sys
import DataBase
from sqlAnalyzer import sqlAnalyzer



class sqlParser:
	"""
		how to implement...

		the part of SELECT and FROM maybe is easy to work, but the most important part is
		the WHERE 

		be careful! the list will contain a empty string. do some exception for it.

	"""
	def __init__(self, DataBase, attribList, tableList, conditionList):
		self.mFromTable = {} # ex. E : EMPLOYEE, but if no alias, it will EMPLOYEE : EMPLOYEE
		self.DB = DataBase
		self.mTable = DataBase.getTable()
		self.mattribList = attribList
		self.mtableList = tableList
		self.mconditionList = conditionList
		self.mresultTable = [] # use a list of dict to express the result table
	
	def strToNumber(self, str):
		str = str.replace(',', '') # ex. transfer 123,456 to 123456
		if re.search('[^0-9\.]+',str):
			return str
		else:
			return float(str)

	def parseSelect(self, innerList):
		''' the possible aggregate function, *, attribute '''

		aggregate={
		'SUM': False,
		'MAX': False,
		'MIN': False,
		'AVG': False,
		'COUNT': False
		}
		
		aggregateFunc = lambda token: sorted([ self.strToNumber( rowData[token] ) for rowData in self.mresultTable ])
		# the above will be used in aggregate function
		resultTable = []

		for token in innerList:
			if token!='':
				if token == '*':
					if aggregate['COUNT']:
						aCount = len(self.mresultTable)
						if resultTable==[]:
							resultTable.append( {'COUNT('+token+')' : aCount } )
						else:
							for index in range( len(resultTable) ):
								resultTable[index].update( {'COUNT('+token+')' : aCount } )
						aggregate['COUNT'] = False
					else:
						resultTable = self.mresultTable[:]
				elif token in 'SUM AVG MAX MIN COUNT'.split(' '):
					aggregate[token] = True
				else: # attribute
					if '.' in token:
						token = token.split('.')[1]

					#add the aggregate function here
					if aggregate['SUM']:
						aSum = sum( sorted(aggregateFunc(token)) )
						if resultTable==[]:
							resultTable.append( {'SUM('+token+')' : aSum} )
						else:
							for index in range( len(resultTable) ):
								resultTable[index].update( {'SUM('+token+')' : aSum} )
						
						aggregate['SUM'] = False
						
					elif aggregate['AVG']:
						aList = aggregateFunc(token)
						aAvg = float( sum(aList) )/float( len(aList) )
						if resultTable==[]:
							resultTable.append( {'AVG('+token+')' : aAvg} )
						else:
							for index in range( len(resultTable) ):
								resultTable[index].update( {'AVG('+token+')' : aAvg} )
						
						aggregate['AVG'] = False
						
					elif aggregate['MAX']:
						aMax = sorted(aggregateFunc(token))[-1]
						if resultTable==[]:
							resultTable.append( {'MAX('+token+')' : aMax} )
						else:
							for index in range( len(resultTable) ):
								resultTable[index].update( {'MAX('+token+')' : aMax} )
								
						aggregate['MAX'] = False
						
					elif aggregate['MIN']:
						aMin = sorted(aggregateFunc(token))[0]
						if resultTable==[]:
							resultTable.append( {'MIN('+token+')' : aMin} )
						else:
							for index in range( len(resultTable) ):
								resultTable[index].update( {'MIN('+token+')' : aMin} )
								
						aggregate['MIN'] = False
						
					elif aggregate['COUNT']:
						aCount = len(aggregateFunc(token))
						if resultTable==[]:
							resultTable.append( {'COUNT('+token+')' : aCount} )
						else:
							for index in range( len(resultTable) ):
								resultTable[index].update( {'COUNT('+token+')' : aCount} )
								
						aggregate['COUNT'] = False
						
					else:
						if resultTable==[]:
							for rowData in self.mresultTable:
								resultTable.append( {token:rowData[token]} )
						else:
							for index in range(len(resultTable)):
								resultTable[index].update( {token : self.mresultTable[index][token]} )

		self.mresultTable = resultTable[:]


	def parseFrom(self):
		''' use a dict to record the map of alias and true name '''
		tableName=''

		for innerList in self.mtableList:
			for token in innerList:
				#the first must be a table name
				#the next you will encounter a , or a alias
				if token!='':
					if self.DB.isTable(token):
						if tableName != '':
							self.mFromTable[tableName] = tableName # a tableName to tableName
						tableName = token
					else:#there is one more possibility
						self.mFromTable[token] = tableName # a lias to tableName
						tableName=''
			if tableName != '':
				self.mFromTable[tableName]=tableName


	def inWhichFromTable(self, token):
		'''
			be used in parseWhere, parse something like E.NUM or NUM
			it will automatically change the alias E to the true table name
			or find which table in FROM condition contain attribute NUM

			return a tuple ( tableName, token)
		'''
		if '.' in token:
			return self.mFromTable[ token.split('.')[0] ], token.split('.')[1]
		else:
			for tableName in self.mFromTable.values():
				if token in self.mTable[tableName][0]:
					return tableName, token
			return '', token

	def parseWhere(self, innerList):
		''' judge it is a join condition or select condition '''

		encouterAND = False
		encouterOR = False

		opPartition = {
		'=' : lambda token : token.partition('='),
		'>' : lambda token : token.partition('>'),
		'<' : lambda token : token.partition('<'),
		'>=': lambda token : token.partition('>='),
		'<=': lambda token : token.partition('<='),
		'!=': lambda token : token.partition('!=')
		} # return a tuple a, b, c

		attribBeforeIN=''
		notIN = False

		for token in innerList:
			if token !='':

				if token == 'TRUE':
					for tablename in self.mFromTable.values():
						resultTable = self.mresultTable[:] # for temp use, remember to use copy
						for rowAttrib in self.mTable[tablename]:
							if self.mresultTable != []:
								for resultRow in self.mresultTable:
									resultRow.update(rowAttrib)
									resultTable.append( resultRow.copy() )
							else:
								resultTable.append(rowAttrib.copy())
						self.mresultTable = resultTable[:]

				elif re.search('[=<>!]+',token) != None: 
					if re.search('[=<>!]+',token).group(0) == '=': #means the input form is xx=xx AND. not xx = xx AND
						lhs, mid, rhs = opPartition['='](token)
						#a situation needed to be considered. ex. rhs=" 'hello' ", then change to " hello "
						if "'" in rhs or '"' in rhs: 
							rhs=rhs[1:len(rhs)-1]

						tableOflhs, lhs = self.inWhichFromTable(lhs)
						tableOfrhs, rhs = self.inWhichFromTable(rhs)
					

						if tableOflhs!='' and tableOfrhs!='': #means this is a join condition
							resultTable = []
							
							if encouterAND:
								for row in self.mresultTable:
									for rData in self.mTable[tableOfrhs]:
										if row[lhs]==rData[rhs]:
											row.update(rData)
											resultTable.append( row.copy() )

							elif encouterOR:
								pass
							else:
								for lData in self.mTable[tableOflhs]:
									for rData in self.mTable[tableOfrhs]:
										#well, actuall, the double for loop is like a cardison product
										if lData[lhs]==rData[rhs]:
											clData = lData.copy()
											clData.update(rData)
											#here is a bug
											resultTable.append(clData)

							self.mresultTable = resultTable[:]

							encouterAND = False
							encouterOR = False			
						else: # a select condition. table.attribute = context
							if self.mresultTable != []:
								resultTable = []

								for lData in self.mresultTable:
									if lData[lhs] == rhs:
										resultTable.append(lData)

								self.mresultTable = resultTable[:]

							else:
								for lData in self.mTable[tableOflhs]:
									if lData[lhs] == rhs:
										clData = lData.copy()
										self.mresultTable.append(clData)
										
					else:
						#select condition, the number compare?
						lhs=''
						mid=''
						rhs=''
					
						op = re.search('[=<>!]+',token).group(0)
						lhs, mid, rhs = opPartition[op](token)

						if "'" in rhs or '"' in rhs: 
							rhs=rhs[1:len(rhs)-1]

						tableOflhs, lhs = self.inWhichFromTable(lhs)
						tableOfrhs, rhs = self.inWhichFromTable(rhs)

						if mid == '>':
							if self.mresultTable != []:
								resultTable = []

								for lData in self.mresultTable:
									if float(lData[lhs]) > float(rhs):
										resultTable.append(lData)
								self.mresultTable = resultTable[:]
							else:
								for lData in self.mTable[tableOflhs]:
									if float(lData[lhs]) > float(rhs):
										clData = lData.copy()
										self.mresultTable.append(clData)

						elif mid == '<':
							if self.mresultTable != []:
								resultTable = []

								for lData in self.mresultTable:
									if float(lData[lhs]) < float(rhs):
										resultTable.append(lData)
								self.mresultTable = resultTable[:]
							else:
								for lData in self.mTable[tableOflhs]:
									if float(lData[lhs]) < float(rhs):
										clData = lData.copy()
										self.mresultTable.append(clData)

						elif mid == '>=':
							if self.mresultTable != []:
								resultTable = []

								for lData in self.mresultTable:
									if float(lData[lhs]) >= float(rhs):
										resultTable.append(lData)
								self.mresultTable = resultTable[:]
							else:
								for lData in self.mTable[tableOflhs]:
									if float(lData[lhs]) >= float(rhs):
										clData = lData.copy()
										self.mresultTable.append(clData)
						elif mid == '<=':
							if self.mresultTable != []:
								resultTable = []

								for lData in self.mresultTable:
									if float(lData[lhs]) <= float(rhs):
										resultTable.append(lData)
								self.mresultTable = resultTable[:]
							else:
								for lData in self.mTable[tableOflhs]:
									if float(lData[lhs]) <= float(rhs):
										clData = lData.copy()
										self.mresultTable.append(clData)
						elif mid == '!=':
							if self.mresultTable != []:
								resultTable = []

								for lData in self.mresultTable:
									if float(lData[lhs]) != float(rhs):
										resultTable.append(lData)
								self.mresultTable = resultTable[:]
							else:
								for lData in self.mTable[tableOflhs]:
									if float(lData[lhs]) != float(rhs):
										clData = lData.copy()
										self.mresultTable.append(clData)

				elif self.inWhichFromTable(token)[0]!='': # means found
					attribBeforeIN = token

				elif token =='NOT': # for not in
					notIN = True

				elif token =='IN':
					resultTable = []

					table, attribBeforeIN = self.inWhichFromTable(attribBeforeIN)

					for row in self.mresultTable:
						for valueOfIN in row.values():
							for data in self.mTable[table]:
								if notIN:
									if data[attribBeforeIN]!=valueOfIN:
										resultTable.append( data.copy() )
								else:
									if data[attribBeforeIN]==valueOfIN:
										resultTable.append( data.copy() )
					
					notIN = False
					self.mresultTable = resultTable[:]

				elif token == 'AND':
					encouterAND = True

				elif token == 'OR':
					encouterOR = True

				else: # xx = xx AND
					pass

	def startParse(self):
		''' use for loop to do nested sql '''
		self.parseFrom() #need to parse whole first

		for layer in range(len(self.mtableList)):
			self.parseWhere(self.mconditionList[layer])
			self.parseSelect(self.mattribList[layer])


	def getResult(self):
		return self.mresultTable




if __name__ == "__main__":
	''' do some unit test to make sure this is ok'''

	sqlInput=[]
	sqlInput.append("SELECT Dname, Sname FROM divinity D has_skill H skill S WHERE D.DID=H.DID and h.sid=s.sid and dname='michael'")
	sqlInput.append("SELECT INAME, PRICE FROM IVENTORY I DIVINITY D HAS_EQUIP HE WHERE HE.DID=D.DID AND HE.IID=I.IID")
	sqlInput.append("SELECT *  FROM DIVINITY D WHERE D.DID IN (SELECT HS.DID FROM HAS_SKILL HS WHERE HS.SID IN (SELECT S.SID FROM SKILL S WHERE S.DAMAGE>=20))")
	sqlInput.append("SELECT * FROM EMPLOYEE E, WORKS_ON W, project P WHERE Dno=5 and E.SSN=W.ESSN AND W.PNO=P.PNUMBER AND HOURS>10 AND Pname='ProductX' ")


	db = DataBase.DataBase('DataBase.xml')
	db.createTable()

	table=db.getTable()


	analyzer = sqlAnalyzer(sqlInput[2])
	analyzer.startAnalyze()

	print(analyzer.getAttribList())
	print(analyzer.getTableList())
	print(analyzer.getConditionList())
	print('================================')

	parser = sqlParser(db, analyzer.getAttribList(), analyzer.getTableList(), analyzer.getConditionList())
	parser.startParse()
	print( db.outputTable(parser.getResult()))
		
	#check the list and table, first