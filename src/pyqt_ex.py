from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import operator


class MyApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.exitaction=QAction(QIcon('logo.ico'),'Exit',self)
        self.exitaction.setShortcut('Crtl+Q')
        self.exitaction.setStatusTip('Exit Application')
        self.exitaction.triggered.connect(QApplication.quit)
        
        self.menuBar().setNativeMenuBar(False)
        self.filemenu=self.menuBar().addMenu('&File')
        self.filemenu.setStatusTip('Look for File Menu')
        self.filemenu.addAction(self.exitaction)
        
        btn=QPushButton('Quit',self)
        btn.move(200,150)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QApplication.instance().quit)
        QToolTip.setFont(QFont('SansSerif', 15))
        btn.setToolTip('Hello')
        
        self.btmprbar=QProgressBar(self)
        self.statusBar().setStyleSheet('border :1px solid;')
        self.statusBar().addPermanentWidget(self.btmprbar)
        self.statusBar().showMessage('Ready')

        self.setWindowTitle('Signal and Slot')
        self.move(0,0)
        self.resize(400,300)
        self.setWindowIcon(QIcon('checkbox/logo.png'))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())