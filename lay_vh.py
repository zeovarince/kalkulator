import sys
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTabWidget,
    QListWidget,
    QMessageBox,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator Sederhana")
        self.setGeometry(200, 200, 300, 300)

        # ====== TAB WIDGET ======
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tab 1: Kalkulator
        self.calc_tab = QWidget()
        self.tabs.addTab(self.calc_tab, "Kalkulator")

        # Tab 2: Riwayat
        self.history_tab = QWidget()
        self.tabs.addTab(self.history_tab, "Riwayat")

        # ====== Kalkulator ======
        self.output = QLineEdit("0")
        self.output.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.output.setReadOnly(True)
        self.output.setFixedHeight(50)

        # ====== Tombol ======
        self.cn = QPushButton("CN")
        self.bagi = QPushButton("/")
        self.multi = QPushButton("*")
        self.del_btn = QPushButton("DEL")

        self.six = QPushButton("6")
        self.eight = QPushButton("8")
        self.nine = QPushButton("9")
        self.min = QPushButton("-")

        self.two = QPushButton("2")
        self.three = QPushButton("3")
        self.four = QPushButton("4")
        self.add = QPushButton("+")

        self.one = QPushButton("1")
        self.zero = QPushButton("0")
        self.dot = QPushButton(".")
        self.equal = QPushButton("=")

        # ====== Layout Vertikal (utama) ======
        background = QVBoxLayout()
        background.addWidget(self.output)

        # ====== Baris-baris tombol ======
        row1 = QHBoxLayout()
        for b in [self.cn, self.bagi, self.multi, self.del_btn]:
            row1.addWidget(b)

        row2 = QHBoxLayout()
        for b in [self.six, self.eight, self.nine, self.min]:
            row2.addWidget(b)

        row3 = QHBoxLayout()
        for b in [self.two, self.three, self.four, self.add]:
            row3.addWidget(b)

        row4 = QHBoxLayout()
        for b in [self.one, self.zero, self.dot, self.equal]:
            row4.addWidget(b)

        # ====== Tambahkan semua baris ke VBox ======
        background.addLayout(row1)
        background.addLayout(row2)
        background.addLayout(row3)
        background.addLayout(row4)

        self.calc_tab.setLayout(background)

        # ====== Riwayat ======
        self.history_list = QListWidget()
        layout_history = QVBoxLayout()
        layout_history.addWidget(QLabel("Riwayat Perhitungan:"))
        layout_history.addWidget(self.history_list)
        self.history_tab.setLayout(layout_history)

        # ====== Sinyal Tombol ======
        for tombol in (self.zero, self.one, self.two, self.three,
                       self.four, self.six, self.eight, self.nine):
            tombol.clicked.connect(self.pushBut)

        for op in (self.add, self.min, self.multi, self.bagi, self.dot):
            op.clicked.connect(self.pushBut)

        self.equal.clicked.connect(self.pushBut)
        self.cn.clicked.connect(self.clear_output)
        self.del_btn.clicked.connect(self.delete_last)

        # ====== Menu Bar ======
        self.create_menu()

    # ====== Fungsi Menu ======
    def create_menu(self):
        menuBar = self.menuBar()
        file_menu = menuBar.addMenu("File")
        exit_action = QAction("Keluar", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    # Menu Operasi
        operasi_menu = menuBar.addMenu("Operasi")

        # Tambahkan semua operasi ke menu
        ops = {
            "Tambah (+)": "+",
            "Kurang (-)": "-",
            "Kali (*)": "*",
            "Bagi (/)": "/",
            "Hapus (DEL)": "DEL",
            "Clear (CN)": "CN",
        }

        for nama, simbol in ops.items():
            act = QAction(nama, self)
            act.triggered.connect(lambda _, s=simbol: self.menu_operasi(s))
            operasi_menu.addAction(act)

    def menu_operasi(self, simbol):
        """Menjalankan operasi dari menu"""
        if simbol == "CN":
            self.clear_output()
        elif simbol == "DEL":
            self.delete_last()
        else:
            # Sama seperti tombol operasi
            front = self.output.text()
            if self.output.text() == "0":
                if simbol == "-":
                    self.output.setText("-")
                else:
                    self.output.setText("0" + simbol)
            elif front[-1] in ["+", "-", "*", "/"]:
                self.output.setText(front[:-1] + simbol)
            else:
                self.output.setText(front + simbol)        

    def show_about(self):
        QMessageBox.information(
            self,
            "Tentang",
            "Kalkulator Sederhana\nDibuat dengan PyQt6."
        )

    # ====== Kalkulator ======
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
                # Tambah ke Riwayat
                self.history_list.addItem(f"{front} = {hasil}")
            return
        self.output.setText(front + text)

    def count(self, expr: str):
        try:
            return eval(expr, {"__builtins__": None}, {})
        except Exception:
            return None

    def clear_output(self):
        self.output.setText("0")

    def delete_last(self):
        teks = self.output.text()
        if len(teks) > 1:
            self.output.setText(teks[:-1])
        else:
            self.output.setText("0")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())