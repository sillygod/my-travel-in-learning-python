'''
    http://pyqt.sourceforge.net/Docs/PyQt4/qgridlayout.html#addWidget-3
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import platform
import os
from urllib import request
import copy



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
        '''only not animated image can be saved
        '''
        if not isinstance(self._container, list):
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






class fileBrowser(QTreeView):
    '''
        add an icon to folder, and scrollbar?
        when an item be clicked, it should be enlight
    '''
    def __init__(self, view=None, path=None):
        super().__init__()
        self._path = os.getcwd() if path == None else path
        self._view = view
        self.setHeaderHidden(True) #to hide the header


        self.setContent()
        self.connect(self, SIGNAL('clicked(QModelIndex)'), self.loadContent)



    def loadContent(self, index):
        '''think how to add behavior like windows treeview
        '''
        item = self.model.itemFromIndex(index)
        fname = item.data()
       
        if os.path.isdir(fname):
            self.expand(index)
        elif os.path.splitext(fname)[1].lower() in ''.join(self.retSupFmt()):   #check the extension
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
                name.setIcon(QIcon('./icons/folder-close.png'))
                for inner in self.recursiveLoad(absPath, name):
                    yield inner
            


    def setContent(self):
        self.model = QStandardItemModel(self)
        for item in self.recursiveLoad(self.path):
            self.model.appendRow(item)

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
        add some keyboard control: left key and right key for surfing the image

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

        #add dockwidget
        logDockWidget = QDockWidget("browser", self)
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                      Qt.RightDockWidgetArea)

        logDockWidget.setWidget(self.fileBrowser)
        self.addDockWidget(Qt.LeftDockWidgetArea, logDockWidget)

        
        #create a widget contain filebrowser and view
        #set the layout
        grid = QGridLayout()
        grid.addWidget(self.view, 0, 1, 1, 5)
        self.ctWidget.setLayout(grid)
        self.setCentralWidget(self.ctWidget)
        self.view.show()



    def createAction(self, name, slot):
        '''simple wrap for create an action
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
            self.fileBrowser.path = os.path.dirname(fname)





if __name__ == '__main__':
    app = QApplication(sys.argv)

    obj = mainWindow()
    obj.show()
    sys.exit(app.exec_())