import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator Sederhana")
        self.setGeometry(200, 200, 300, 300)

        # widget tampilan (layar)
        self.output = QLineEdit("0")
        self.output.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.output.setReadOnly(True)
        self.output.setFixedHeight(50)

        # inisialisasi tombol
        self.cn = QPushButton("CN")
        self.add = QPushButton("+")
        self.min = QPushButton("-")
        self.multi = QPushButton("*")
        self.bagi = QPushButton("/")
        self.dot = QPushButton(".")
        self.equal = QPushButton("=")
        self.nine = QPushButton("9")
        self.eight = QPushButton("8")
        self.six = QPushButton("6")
        self.four = QPushButton("4")
        self.three = QPushButton("3")
        self.two = QPushButton("2")
        self.one = QPushButton("1")
        self.zero = QPushButton("0")

        # susunan tombol pakai VBox + HBox
        background = QVBoxLayout()
        background.addWidget(self.output)

        # baris 1
        row1 = QHBoxLayout()
        row1.addWidget(self.cn)
        row1.addWidget(self.add)
        row1.addWidget(self.min)

        # baris 2
        row2 = QHBoxLayout()
        row2.addWidget(self.nine)
        row2.addWidget(self.eight)
        row2.addWidget(self.multi)

        # baris 3
        row3 = QHBoxLayout()
        row3.addWidget(self.six)
        row3.addWidget(self.four)
        row3.addWidget(self.bagi)

        # baris 4
        row4 = QHBoxLayout()
        row4.addWidget(self.three)
        row4.addWidget(self.two)
        row4.addWidget(self.dot)

        # baris 5
        row5 = QHBoxLayout()
        row5.addWidget(self.one)
        row5.addWidget(self.zero)
        row5.addWidget(self.equal)

        # tambahkan semua baris ke layout utama
        background.addLayout(row1)
        background.addLayout(row2)
        background.addLayout(row3)
        background.addLayout(row4)
        background.addLayout(row5)

        # central widget
        central = QWidget()
        central.setLayout(background)
        self.setCentralWidget(central)

        # sambungkan tombol angka
        for tombol in (self.zero, self.one, self.two, self.three,
                       self.four, self.six, self.eight, self.nine):
            tombol.clicked.connect(self.pushBut)

        # sambungkan tombol operator
        for op in (self.add, self.min, self.multi, self.bagi, self.dot):
            op.clicked.connect(self.pushBut)

        # tombol lain
        self.equal.clicked.connect(self.pushBut)
        self.cn.clicked.connect(self.clear_output)

    # fungsi kalkulator
    def pushBut(self):
        operan = ["+", "-", "*", "/"]
        angka = "98643210"
        btn = self.sender()
        if not btn:
            return
        text = btn.text()
        front = self.output.text()

        if self.output.text() == "0" and text in angka:
            self.output.setText(text)
            return
        if text in operan:
            if self.output.text() == "0" and text == "-":
                self.output.setText("-")
            elif front and front[-1] in operan:
                self.output.setText(front[:-1] + text)
            else:
                self.output.setText(front + text)
            return
        if text == "=":
            hasil = self.count(front)
            if hasil is None:
                self.output.setText("Err")
            else:
                self.output.setText(str(hasil))
            return
        self.output.setText(front + text)

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