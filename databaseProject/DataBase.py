'''
	FUNC: read a xml file(database) and transfer it to a list of dictionary type
	note: no case sensitive
	
	I will make a rule about the database in xml form
	ex. 
	____________________________
	Student	|name | ID | score |  and ID is a key
			|aa   | 1  |  10   |
			|bb   | 2  |  20   |

	in XML file, I will use something like the following.
	
	<table name='Student'>
		<data>
			<name>aa</name>
			<ID key='key'>1</ID>
			<score>10</score>
		</data>
		<data>
			<name>bb</name>
			<ID key='key'>2</ID>
			<score>20</score>
		</data>
	</table>

	table data type: a dict contain a dict of list ex. dict[{}:[{}]]
'''
try:
	import xml.etree.cElementTree as eTree
except ImportError:
	import xml.etree.ElementTree as eTree
# the above, try to find the api implemented by C because of the speed consideration
# but in python3.3, you just type import xml.etree.ElementTree. it will automatically to find the best
class DataBase:
	def __init__(self, fileName):
		self.Table = {}
		self.Tree = eTree.parse(fileName)
		
		self.createTable()
	
	def createTable(self):
		'''	start to traverse '''
		for elem in self.Tree.iter(tag='table'):
			tableName=elem.attrib['name'].upper()
			self.Table[tableName] = [] # make a table
			
			for data in elem: # enter the each data of table
				rowAttribute={} # make a new dict
				for attribute in data:
					rowAttribute[attribute.tag.upper()]=attribute.text.upper()
				self.Table[tableName].append(rowAttribute)
	
	def getTable(self):
		''' return a table '''
		return self.Table

	def findAttribInWhichTable(self, attribName):
		result=[]
		for key in self.Table:
			if attribName in self.Table[key][0]:
				result.append(key)
		return result

	def isTable(self, tableName):
		''' check the existence of tableName'''
		return tableName in self.Table

	def outputTable(self, table):
		''' table is a list '''
		outputString=''
		#dynamic to adjust the alignment?
		Alignment = '{:^20}'
		isFirstColumn = True

		if table == []:
			return 'NULL'

		order = table[0].keys()

		for columnName in order:
			if isFirstColumn:
				outputString += Alignment.format(columnName)
				isFirstColumn = False
			else:
				outputString += Alignment.format(columnName)
		outputString += '\n'
		isFirstColumn =True

		for data in table:
			for attrib in order:
				if isFirstColumn:
					outputString += Alignment.format(data[attrib])
					isFirstColumn = False
				else:
					outputString += Alignment.format(data[attrib])

			isFirstColumn = True
			outputString += '\n'

		return outputString
