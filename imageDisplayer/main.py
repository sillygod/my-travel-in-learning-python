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
		self.setSceneRect(0, 0, self.img.size().width(), self.img.size().height())
		self.imgLst = []

		
		if self.img.imageCount()>1:  #self.img.supportsAnimation wierd why jpg is also support?
			super().startTimer(self.img.nextImageDelay())
			self._distractImg()
		else:
			self.addPixmap(QPixmap.fromImageReader(self.img))

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





class mainWindow(QMainWindow):
	'''
		dockwidget can only dock in qmainwindow
	'''

	def __init__(self):
		pass



if __name__ == '__main__':
	app = QApplication(sys.argv)
	obj = imgDisplay('D:/My Pictures/yaumom.jpg')

	view = QGraphicsView(obj)
	view.show()

	sys.exit(app.exec_())