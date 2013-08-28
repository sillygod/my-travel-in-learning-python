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
		self.imgLst = []

		
		if self.img.imageCount()>1:  #self.img.supportsAnimation wierd why jpg is also support?
			super().startTimer(self.img.nextImageDelay())
			self._distractImg()
		else:
			self.addPixmap(QPixmap.fromImageReader(self.img))

	def retRect(self):
		return self.rect

	def _distractImg(self):
		for i in range(self.img.imageCount()):
			self.imgLst.append( QPixmap.fromImageReader(self.img) )
		self._iter = iter(self.imgLst)
			

	def timerEvent(self, QTimerEvent):
		super().timerEvent(QTimerEvent)
		try:
			self.addPixmap(next(self._iter))
		except:
			self._iter = iter(self.imgLst)
			self.addPixmap(next(self._iter))

		self.update()



class fileBrowser:
	'''
		os.listdir(path)
		os.getcwd()
		os.path.isdir() has some function
	'''
	def __init__(self, path=None):
		self._path = getcwd() if path == None else path



	
	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, value):
		self._path = value



class mainWindow(QMainWindow):
	'''
		dockwidget can only dock in qmainwindow

	'''

	def __init__(self):
		super().__init__()
		self.act = {}
		self.view = QGraphicsView()
		menu = self.menuBar()
		
		self.createAction('Open', self.openFile)

		#create menu
		fileMenu = menu.addMenu('&File')
		fileMenu.addAction(self.act['Open'])

		
		self.setCentralWidget(self.view)
		self.view.show()



	def createAction(self, name, slot):
		'''

		'''
		act = QAction(name, self)
		act.triggered.connect(slot)
		self.act['Open'] = act



	def openFile(self):

		supFmt = ('*.{}'.format(bytearray(x).decode()) for x in QImageReader.supportedImageFormats())
		dir = '.'
		filter = 'Images ({})'.format(' '.join(supFmt))
		fname = QFileDialog.getOpenFileName(self, 'open', dir, filter)

		obj = imgDisplay(fname)
		self.view.setScene(obj)
		self.resize(obj.retRect().width(), obj.retRect().height()+50)






if __name__ == '__main__':
	app = QApplication(sys.argv)

	obj = mainWindow()
	obj.show()

	sys.exit(app.exec_())