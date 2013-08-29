'''
	http://pyqt.sourceforge.net/Docs/PyQt4/qgridlayout.html#addWidget-3
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import platform
import os
from urllib import request


class imgDisplay(QGraphicsScene):
	'''
		a displayer for static and animated Pictures
	'''
	def __init__(self, fname, parent=None):
		super().__init__(parent)
		self.img = QImageReader(fname)
		self.rect = QRect(0, 0, self.img.size().width(), self.img.size().height())
		self.setSceneRect(QRectF(self.retRect()))
		self._container = None

		
		if self.img.imageCount()>1:  #self.img.supportsAnimation wierd why jpg is also support?
			super().startTimer(self.img.nextImageDelay())
			self._distractImg()
		else:
			self._container = QPixmap.fromImageReader(self.img)
			self.addPixmap(self._container)

	def saveImg(self, fileName):
		self._container.save(fileName)


	def retRect(self):
		return self.rect

	def _distractImg(self):
		self._container = [ QPixmap.fromImageReader(self.img) for i in range(self.img.imageCount()) ]
		self._iter = iter(self._container)
			

	def timerEvent(self, QTimerEvent):
		super().timerEvent(QTimerEvent)
		try:
			self.addPixmap(next(self._iter))
		except:
			self._iter = iter(self._container)
			self.addPixmap(next(self._iter))

		self.update()



class fileBrowser(QListView):
	'''
		
	'''
	def __init__(self, view=None, path=None):
		super().__init__()
		self._path = os.getcwd() if path == None else path
		self.setContent()
		self._view = view

	
		self.connect(self, SIGNAL('clicked(QModelIndex)'), self.loadContent)


	def loadContent(self, index):
		fname = os.path.join(self.path, index.data())
		if os.path.splitext(fname)[1].lower() in ''.join(self.retSupFmt()):   #check the extension
			obj = imgDisplay(fname)
			self._view.setScene(obj)
		else:
			print('filter')

	def retSupFmt(self):
		''' return a generator of supported file format'''
		return ('*.{}'.format(bytearray(x).decode()) for x in QImageReader.supportedImageFormats())



	def setContent(self):
		self.model = QStandardItemModel(self)

		for fname in os.listdir(self.path):
			name = QStandardItem(fname)
			self.model.appendRow(name)

		self.setModel(self.model)


	
	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, value):
		self._path = value
		self.setContent()



class mainWindow(QMainWindow):
	'''
		dockwidget can only dock in qmainwindow

		mission: add file browser next, and add icon control button as best as I can

	'''

	def __init__(self):
		super().__init__()
		self.act = {}
		self.ctWidget = QWidget()
		self.view = QGraphicsView()
		self.fileBrowser = fileBrowser(self.view)
		
		
		self.createAction('Open', self.openFile)
		self.createAction('Save', self.saveFile)
		#create menu
		menu = self.menuBar()
		fileMenu = menu.addMenu('&File')
		fileMenu.addAction(self.act['Open'])
		fileMenu.addAction(self.act['Save'])

		
		#create a widget contain filebrowser and view
		#set the layout
		grid = QGridLayout()
		grid.addWidget(self.fileBrowser, 0, 0, 1, -1) #-1?
		grid.addWidget(self.view, 0, 1, 1, 5)
		self.ctWidget.setLayout(grid)
		self.setCentralWidget(self.ctWidget)
		self.view.show()



	def createAction(self, name, slot):
		'''

		'''
		act = QAction(name, self)
		act.triggered.connect(slot)
		self.act[name] = act

	def saveFile(self):
		supFmt = ('*.{}'.format(bytearray(x).decode()) for x in QImageReader.supportedImageFormats())
		filter = 'Images ({})'.format(' '.join(supFmt))
		fname = QFileDialog.getSaveFileName(self, 'save', '.', filter)
		if fname:
			self.view.scene().saveImg(fname)



	def openFile(self):

		supFmt = self.fileBrowser.retSupFmt()
		dir = '.'
		filter = 'Images ({})'.format(' '.join(supFmt))
		fname = QFileDialog.getOpenFileName(self, 'open', dir, filter)
		if fname:
			obj = imgDisplay(fname)
			self.view.setScene(obj)
			self.resize(obj.retRect().width(), obj.retRect().height()+50)
			self.fileBrowser.path = os.path.dirname(fname)
			# need to rethink how to resize ....






if __name__ == '__main__':
	app = QApplication(sys.argv)

	obj = mainWindow()
	obj.show()
	sys.exit(app.exec_())