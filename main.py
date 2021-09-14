import sys
import threading

import mips

from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import *
import serial
import queue


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

        self.queue = queue.Queue(10000)
        self.portx = "COM4"
        self.bps = 128000
        self.timex = 10
        self.ser = serial.Serial(self.portx, self.bps, timeout=self.timex)
        threading.Thread(target=self.receive).start()
        self.queuePrint()

    def receive(self):  # 接收函数

        while True:
            while self.ser.inWaiting() > 0:
                myout = self.ser.read(4)
                self.resultAppend(int.from_bytes(myout, byteorder='big', signed=False))

    def sendCode(self, text):  # 发送代码
        self.ser.write(mips.things_to_send(text))

    def sendNum(self, num):  # 发送数字
        self.ser.write(int(num).to_bytes(length=4,byteorder='big',signed=False))

    def initUI(self):

        mainBox = QVBoxLayout()
        self.setFont(QFont("Arial",10,QFont.Bold))

        hbox = QHBoxLayout()

        self.textSend = QLineEdit()
        self.btnCode = QPushButton("COMPILE",self)
        self.btnCode.setFixedWidth(100)
        self.btnSend = QPushButton("SEND")
        self.btnSend.setFixedWidth(100)
        self.btnClear = QPushButton("CLEAR")
        self.btnClear.setFixedWidth(100)

        self.btnClear.clicked.connect(self.btnClearClick)
        self.btnSend.clicked.connect(self.btnSendClick)
        self.btnCode.clicked.connect(self.btnCodeClick)
        self.textSend.returnPressed.connect(self.btnSendClick)

        hbox.addWidget(self.textSend)
        hbox.addWidget(self.btnSend)
        hbox.addWidget(self.btnCode)
        hbox.addWidget(self.btnClear)

        hbox.setAlignment(QtCore.Qt.AlignLeft)

        self.textCode = QTextEdit()
        self.textResult = QTextEdit()

        hboxWidget = QWidget()
        hboxWidget.setLayout(hbox)

        mainBox.addWidget(hboxWidget)
        mainBox.addWidget(QLabel("Code:"))
        mainBox.addWidget(self.textCode)
        mainBox.addWidget(QLabel("Result:"))
        mainBox.addWidget(self.textResult)

        self.setLayout(mainBox)

        self.setFixedHeight(700)
        self.setFixedWidth(700)
        self.setWindowTitle('Mars Simulator')

        self.show()

    def btnCodeClick(self):
        self.sendCode(self.textCode.toPlainText())
        self.btnClearClick()


    def btnSendClick(self):
        if (self.textSend.text().isdigit()) :
            self.sendNum(self.textSend.text())
            self.resultAppend(">> " + self.textSend.text())
            self.textSend.clear()

    def btnClearClick(self):
        self.textSend.clear()
        self.textResult.clear()

    def resultAppend(self, text):
        self.queue.put(text)

    def queuePrint(self):
        threading.Timer(0.01, self.queuePrint).start()
        if (self.queue.empty()) : return
        text = self.queue.get()
        self.textResult.append(str(text))
        self.textResult.moveCursor(QTextCursor.End)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())