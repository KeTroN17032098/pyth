from PyQt5.QtCore import *
from PyQt5.QtGui import QTextBlock
from PyQt5.QtWidgets import *
import sys
import operator


class MyApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lcd = QLCDNumber(self)
        dial = QLineEdit(self)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(dial)
        self.setLayout(vbox)

        dial.in.connect(lcd.display)

        self.setWindowTitle('Signal and Slot')
        self.setGeometry(300, 300, 200, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())