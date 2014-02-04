# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created: Tue Feb  4 21:49:28 2014
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(963, 697)
        MainWindow.setStyleSheet(_fromUtf8("QStatusBar{\n"
                                           "background:rgb(50,50,50);\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar{\n"
                                           "background: rgba(25, 25, 25, 10);\n"
                                           "padding:3px;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::handle:horizontal{\n"
                                           "    background:rgb(50,50,50);\n"
                                           "    min-height:20px;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::handle:vertical{\n"
                                           "    background:rgb(50,50,50);\n"
                                           "    min-height:20px;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::add-line:vertical{\n"
                                           "    background:none;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::add-page:vertical{\n"
                                           "    background:none;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::up-arrow{\n"
                                           "    background:none;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::down-arrow{\n"
                                           "    background:none;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::sub-page:vertical{\n"
                                           "    background:none;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::sub-line:vertical{\n"
                                           "    background:none;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::sub-page:horizontal{\n"
                                           "    background:none;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::sub-line:horizontal{\n"
                                           "    background:none;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::add-line:horizontal{\n"
                                           "    background:none;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar::add-page:horizontal{\n"
                                           "    background:none;\n"
                                           "}\n"
                                           "\n"
                                           "QScrollBar:left-arrow, QScrollBar:right-arrow{\n"
                                           "    background:none;\n"
                                           "}\n"
                                           ""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet(
            _fromUtf8("background:rgb(25,25,25);"))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.treeView = QtGui.QTreeView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setSizeIncrement(QtCore.QSize(0, 0))
        self.treeView.setStyleSheet(_fromUtf8("#treeView{\n"
                                              "border: 2px solid rgb(50,50,50);\n"
                                              "outline: 0;\n"
                                              "}\n"
                                              "\n"
                                              " QTreeView::branch:closed::has-children{\n"
                                              "         image: url(./icons/folder-close.png);\n"
                                              " }\n"
                                              "\n"
                                              " QTreeView::branch:open::has-children{\n"
                                              "         image: url(./icons/folder-open.png);\n"
                                              " }\n"
                                              "\n"
                                              "#treeView::item{\n"
                                              "color:rgba(220,220,220,190);\n"
                                              "}\n"
                                              "\n"
                                              "#treeView::item:selected{\n"
                                              "background:rgb(38, 150, 255);\n"
                                              "}\n"
                                              "\n"
                                              "#treeView::item:hover{\n"
                                              "color:rgba(220,220,220,255);\n"
                                              "border:none;\n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "\n"
                                              ""))
        self.treeView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.treeView.header().setVisible(False)
        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(250, 25))
        self.pushButton.setStyleSheet(_fromUtf8("#pushButton{\n"
                                                "border: 2px solid rgb(50,50,50);\n"
                                                "background: rgba(61, 139, 198, 150);\n"
                                                "color: rgb(35, 35, 35);\n"
                                                "}\n"
                                                "\n"
                                                "#pushButton:hover{\n"
                                                "background:rgba(61, 139, 198, 255);\n"
                                                "}"))
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 4, 2, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(250, 25))
        self.lineEdit.setSizeIncrement(QtCore.QSize(0, 0))
        self.lineEdit.setStyleSheet(_fromUtf8("#lineEdit{\n"
                                              "border:2px solid rgb(50,50,50);\n"
                                              "padding: 1px;\n"
                                              "color:rgb(70,70,70);\n"
                                              "}\n"
                                              "\n"
                                              "#lineEdit:hover{\n"
                                              "background:rgba(50,50,50,100);\n"
                                              "}"))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 4, 0, 1, 2)
        self.view = QtGui.QGraphicsView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.view.sizePolicy().hasHeightForWidth())
        self.view.setSizePolicy(sizePolicy)
        self.view.setMinimumSize(QtCore.QSize(0, 0))
        self.view.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.view.setSizeIncrement(QtCore.QSize(0, 0))
        self.view.setStyleSheet(_fromUtf8("#view{\n"
                                          "    border:2px solid rgb(50,50,50);\n"
                                          "}\n"
                                          "\n"
                                          "\n"
                                          ""))
        self.view.setFrameShadow(QtGui.QFrame.Plain)
        self.view.setMidLineWidth(0)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.view.setObjectName(_fromUtf8("view"))
        self.gridLayout.addWidget(self.view, 0, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 963, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(
            _translate("MainWindow", "grab clipboard", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionOpen.setText(_translate("MainWindow", "open", None))
        self.actionSave.setText(_translate("MainWindow", "save", None))
        self.actionExit.setText(_translate("MainWindow", "exit", None))
