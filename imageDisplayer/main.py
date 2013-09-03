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






class fileBrowser(QListView):
    '''
        add an icon to folder, and scrollbar?
        when an item be clicked, it should be enlight
        can QlistView be folded?
    '''
    def __init__(self, view=None, path=None):
        super().__init__()
        self._path = os.getcwd() if path == None else path
        self._view = view



        self.setContent()
        self.connect(self, SIGNAL('clicked(QModelIndex)'), self.loadContent)



    def loadContent(self, index):
        '''think how to add behavior like windows treeview
        '''
        item = self.model.itemFromIndex(index)
        fname = item.data()
       
        indent = '    '

        if os.path.isdir(fname):
            item.setIcon(QIcon('./icons/folder-open.png'))
            for ifname in os.listdir(fname):
                name = QStandardItem(indent+ifname)
                name.setData( os.path.join(fname, ifname))
                exist = self.model.findItems(indent+ifname)
                if  exist == []:
                    self.model.insertRow(index.row()+1, name)
                else:
                    self.model.removeRow(exist[0].row())

            # item = copy._copy_with_constructor(item)
        
            # self.model.removeRow(index.row())
            # self.model.insertRow(index.row(), item)
            
            # send signal dataChanged()?

        elif os.path.splitext(fname)[1].lower() in ''.join(self.retSupFmt()):   #check the extension
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
            absPath = os.path.join(self.path, fname)
            name = QStandardItem(fname)
            if os.path.isdir(absPath):
                name.setIcon(QIcon('./icons/folder-close.png'))

            name.setData( absPath ) #set the absolute path in dat
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

        add some keyboard control: left key and right key for surfing the image

        note:
            now, I still don't know why grid layout is strange

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
        grid.addWidget(self.fileBrowser, 0, 0, 1, 2) #-1?
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