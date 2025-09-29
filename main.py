import sys
import re
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QTabWidget,
    QListWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator Sederhana")
        self.setGeometry(200, 200, 300, 300)

        #widget tampilan
        self.output = QLineEdit("0")
        self.output.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.output.setReadOnly(True)
        self.output.setFixedHeight(50)

        #layout tombol
        
        #Iniliasi
        num_ops = QGridLayout()
        self.cn  = QPushButton("CN")
        self.add = QPushButton("+")
        self.min = QPushButton("-")
        self.multi = QPushButton("*")
        self.bagi = QPushButton("/")
        self.dot = QPushButton(".")
        self.equal = QPushButton("=")
        self.nine  = QPushButton("9")
        self.eight = QPushButton("8")
        self.six   = QPushButton("6")
        self.four  = QPushButton("4")
        self.three = QPushButton("3")
        self.two   = QPushButton("2")
        self.one   = QPushButton("1")
        self.zero  = QPushButton("0")

        # Button Angka dan Operator
        num_ops.addWidget(self.cn, 1, 0)
        num_ops.addWidget(self.add, 1, 1)
        num_ops.addWidget(self.min, 1, 2)
        num_ops.addWidget(self.multi, 2, 2)
        num_ops.addWidget(self.bagi, 3, 2)
        num_ops.addWidget(self.dot, 4, 2)
        num_ops.addWidget(self.equal, 5, 2)
        num_ops.addWidget(self.nine, 2, 0)
        num_ops.addWidget(self.eight, 2, 1)
        num_ops.addWidget(self.six, 3, 0)
        num_ops.addWidget(self.four, 3, 1)
        num_ops.addWidget(self.three, 4, 0)
        num_ops.addWidget(self.two, 4, 1)
        num_ops.addWidget(self.one, 5, 0)
        num_ops.addWidget(self.zero, 5, 1)

        #susunan vertikal
        background = QVBoxLayout()
        background.addWidget(self.output)
        background.addLayout(num_ops)

        #central widget
        central = QWidget()
        central.setLayout(background)
        self.setCentralWidget(central)

        # sambungkan Untuk Memanggil Funsi 
        for tombol in (self.zero, self.one, self.two, self.three,
                    self.four, self.six, self.eight, self.nine):
            tombol.clicked.connect(self.pushBut)
            
        for op in (self.add, self.min, self.multi, self.bagi, self.dot):
            op.clicked.connect(self.pushBut)
        self.equal.clicked.connect(self.pushBut)
        self.cn.clicked.connect(self.clear_output)

    #Machine Kalkulator
    def pushBut(self):
        operan=["+","-","*","/"]
        angka="98643210"
        btn = self.sender()   
        if not btn:
            return
        text = btn.text()
        front=self.output.text()
        if self.output.text() == "0" and text in angka:
            self.output.setText(text)
            return
        if text in operan:
            if self.output.text() == "0" and text=="-":
                self.output.setText("-")
            elif front and front[-1] in operan:
                self.output.setText(front[:-1]+text)
            else:
                self.output.setText(front+text)
            return
        if text=="=":
            hasil=self.count(front)
            if hasil == None:
                self.output.setText("Err")
            else:
                self.output.setText(str(hasil))
            return
        self.output.setText(front+text)
            

    def count(self, expr: str):
        try:
            return eval(expr, {"__builtins__": None}, {})
        except Exception:
            return None
        
    def clear_output(self):
        self.output.setText("0")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()