'''
	first time to use python tkinter...
	This is an interface for typing sql query and then show the result

	issue:
		so hard to find a document, lol.

		there are three method to show the component
		pack()
		grid()
		place()

	reference links 
	http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
	http://www.python-course.eu/tkinter_layout_management.php
	http://fossies.org/dox/Python-3.3.0/classtkinter_1_1tix_1_1ScrolledWindow.html

	my thought: tkinter is a suck= =, not only so hard to use but also less reference
	and more even, the official document is ....

'''
from DataBase import DataBase
from sqlAnalyzer import sqlAnalyzer
from sqlParser import sqlParser

# the standard gui library in python
from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from tkinter import tix

# need to design a frame
class scrolledCanvas:
	''' to make a excel-like table'''
	def __init__(self, master, swidth=860, sheight=640):
		self.canvas = Canvas(master, width=swidth-20, height=sheight-20)
		self.frame = Frame(self.canvas)
		self.vscroll = Scrollbar(master, command=self.canvas.yview)
		self.hscroll = Scrollbar(master, orient=HORIZONTAL, command=self.canvas.xview)
		self.canvas.configure(yscrollcommand=self.vscroll.set)
		self.canvas.configure(xscrollcommand=self.hscroll.set)

		self.vscroll.place(x=swidth-20, y=0, width=20, height=sheight)
		self.hscroll.place(x=0, y=sheight-20, width=swidth, height=20)
		self.canvas.pack(side='top', anchor='w')
		self.canvas.create_window((0,0), window=self.frame, anchor='nw')

		self.frame.bind('<Configure>', self.onFrameConfigure)


	def populate(self, table):

		c, r = 0, 0
		for columnName in table[0].keys(): #output column name
			Label(self.frame, text=columnName, relief=RIDGE, width=20).grid(row=r, column=c)
			c+=1

		c, r = 0, 1
		#output the data
		for data in table:
			for attrib in data.keys():
				Label(self.frame, text=data[attrib], relief=RIDGE, width=20).grid(row=r, column=c)
				c+=1
			r+=1
			c=0

	def onFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox('all'))
		


class sqlApp:
	'''
		responsible for the control of interface
	'''

	def __init__(self, master=None):
		self.db = DataBase("DataBase.xml")
		
		self.master = master
		self.NB = ttk.Notebook(self.master)

		self.mainFrame = Frame(self.master)
		self.sqlInputEntry = Entry(self.mainFrame, relief=SUNKEN) 
		self.sqlInputEntry.bind('<Return>', self.startQuery)
		

		self.resetButton = Button(self.mainFrame, text='reset', command=self.reset)
		self.startButton = Button(self.mainFrame, text='start', command=self.startQuery)
		self.resultWindow = Frame(self.mainFrame, relief=RIDGE, borderwidth=2)


		self.DBtableCanvas = {} # store the db table cnavas
		self.DBtableFrame = {}


	def reset(self):
		self.sqlInputEntry.delete(0, END)
		self.resultWindow.destroy()
		self.resultWindow = Frame(self.mainFrame, relief=RIDGE, borderwidth=2)
		self.resultWindow.place(x=80, y=80, width=700, height=500)

			
	def startQuery(self, event=None):
		analyzer =sqlAnalyzer( self.sqlInputEntry.get() )
		analyzer.startAnalyze()
		parser = sqlParser(self.db, analyzer.getAttribList(), analyzer.getTableList(), analyzer.getConditionList() )
		parser.startParse()

		resultCanvas = scrolledCanvas(self.resultWindow, 700, 500)
		resultCanvas.populate(parser.getResult())
		



	def display(self):
		self.mainFrame.place(width=860, height=640)
		self.sqlInputEntry.place(x=90, y=30, width=660, height=25)
		self.resetButton.place(x=760, y=30, width=45, height=25)
		self.startButton.place(x=815, y=30, width=40, height=25)
		self.resultWindow.place(x=80, y=80, width=700, height=500)

		
		self.NB.add(child=self.mainFrame, text='SQL query') #!!!!! very important you must call place() before add them		
		table = self.db.getTable()
		for tableName in table.keys():
			self.DBtableFrame[tableName] = Frame(self.master)
			self.DBtableCanvas[tableName]=scrolledCanvas( self.DBtableFrame[tableName], 855, 615)
			self.DBtableCanvas[tableName].populate(table[tableName])
			self.NB.add(child=self.DBtableFrame[tableName], text=tableName)


		self.NB.place(width=860, height=640)




if __name__ == '__main__':
	root = Tk()
	root.geometry("860x640")
	root.title('SQL query program')
	app = sqlApp(root)
	app.display()
	root.mainloop()
	
	
