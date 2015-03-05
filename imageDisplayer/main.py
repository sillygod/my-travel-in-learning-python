'''
    http://pyqt.sourceforge.net/Docs/PyQt4/qgridlayout.html#addWidget-3
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
import io
from view import Ui_MainWindow

if sys.version_info.major >= 3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import HTTPError
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import HTTPError
    from urllib import urlencode


class imgDisplay(QGraphicsScene):

    '''
        a displayer for static and animated Pictures
    '''

    def __init__(self, fname=None, byteIO=None, parent=None):
        super(imgDisplay, self).__init__(parent)
        self.img = None
        self._container = None

        if fname:
            self.img = QImageReader(fname)
        elif byteIO:
            self.img = QImageReader(byteIO)

        if self.img:
            self.rect = QRect(
                0, 0, self.img.size().width(), self.img.size().height())
            self.setSceneRect(QRectF(self.retRect()))
            self._container = None

            # self.img.supportsAnimation wierd why jpg is also support?
            if self.img.imageCount() > 1:
                super().startTimer(self.img.nextImageDelay())
                self._distractImg()
            else:
                self._container = QPixmap.fromImageReader(self.img)
                self.addPixmap(self._container)

    def fromQimage(self, img):
        self.img = img
        self._container = QPixmap.fromImage(self.img)
        self.addPixmap(self._container)

    def saveImg(self, fileName):
        '''only not animated image can be saved
        '''
        if not isinstance(self._container, list):
            self._container.save(fileName)

    def retRect(self):
        return self.rect

    def _distractImg(self):
        self._container = [QPixmap.fromImageReader(self.img)
                           for i in range(self.img.imageCount())]
        self._iter = iter(self._container)

    def timerEvent(self, QTimerEvent):
        super().timerEvent(QTimerEvent)
        try:
            self.addPixmap(next(self._iter))
        except:
            self._iter = iter(self._container)
            self.addPixmap(next(self._iter))

        self.update()


class fileBrowser(object):

    '''
        add an icon to folder, and scrollbar?
        when an item be clicked, it should be enlight
    '''

    def __init__(self, view=None, path=None, treeview=None):
        super(fileBrowser, self).__init__()
        self._path = os.getcwd() if path is None else path
        self._view = view

        self._treeview = treeview
        self._treeview.connect(self._treeview, SIGNAL('clicked(QModelIndex)'), self.loadContent)
        self.setContent()

    def loadContent(self, index):
        '''think how to add behavior like windows treeview
        '''
        item = self.model.itemFromIndex(index)
        fname = item.data()

        if os.path.isdir(fname):
            self._treeview.expand(index)
        # check the extension
        elif os.path.splitext(fname)[1].lower() in ''.join(self.retSupFmt()):
            obj = imgDisplay(fname)
            self._view.setScene(obj)
        else:
            print('filter')

    def retSupFmt(self):
        ''' return a generator of supported file format'''
        return ('*.{}'.format(bytearray(x).decode()) for x in QImageReader.supportedImageFormats())

    def recursiveLoad(self, path, parent=None):
        '''path -- absPath
        '''
        for fname in os.listdir(path):
            absPath = os.path.join(path, fname)
            name = QStandardItem(fname)
            name.setData(absPath)

            if parent:
                parent.appendRow(name)
            else:
                yield name

            if os.path.isdir(absPath):
                for inner in self.recursiveLoad(absPath, name):
                    pass

    def setContent(self):
        self.model = QStandardItemModel(self._treeview)
        for item in self.recursiveLoad(self.path):
            self.model.appendRow(item)

        self._treeview.setModel(self.model)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value
        self.setContent()


class mainWindow(QMainWindow, Ui_MainWindow):

    '''dockwidget can only dock in qmainwindow
    add some keyboard control: left key and right key for surfing the image
    '''

    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)
        self.act = {}
        self.fileBrowser = fileBrowser(view=self.view, treeview=self.treeView)

        # self.createAction('Open', self.openFile)
        # self.createAction('Save', self.saveFile)

        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)

        self.connect(self.pushButton, SIGNAL('clicked()'), self.getImageFromClipboard)
        self.connect(self.lineEdit, SIGNAL('returnPressed()'), self.getInputContent)

        self.view.show()

    def getImageFromClipboard(self):
        img = app.clipboard().image()
        obj = imgDisplay()
        obj.fromQimage(img)
        self.view.setScene(obj)

    def getInputContent(self):
        '''
            notice
            don't write QBuffer( QByteArray(img_file.read()))
            this will cause some problem...
        '''
        webImg = urlopen(self.lineEdit.text())
        img_file = io.BytesIO(webImg.read())
        data = QByteArray(img_file.read())
        temp = QBuffer(data)

        obj = imgDisplay(byteIO=temp)
        self.view.setScene(obj)

    def createAction(self, name, slot):
        '''simple wrap for create an action
        '''
        act = QAction(name, self)
        act.triggered.connect(slot)
        self.act[name] = act

    def saveFile(self):
        supFmt = ('*.{}'.format(bytearray(x).decode())
                  for x in QImageReader.supportedImageFormats())
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
            self.fileBrowser.path = os.path.dirname(fname)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    obj = mainWindow()
    obj.show()
    sys.exit(app.exec_())
