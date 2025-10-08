import sys
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
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

        # ====== Display ======
        self.output = QLineEdit("0")
        self.output.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.output.setReadOnly(True)
        self.output.setFixedHeight(50)

        # ====== Buat Tombol ======
        tombol_labels = [
            ["CN", "/", "*", "DEL"],
            ["6", "8", "9", "-"],
            ["2", "3", "4", "+"],
            ["1", "0", ".", "="],
        ]

        self.tombol_map = {}  # simpan tombol untuk koneksi sinyal nanti

        # ====== Susun Tombol dengan Grid ======
        grid = QGridLayout()
        for row, baris in enumerate(tombol_labels):
            for col, teks in enumerate(baris):
                btn = QPushButton(teks)
                btn.setFixedHeight(45)
                grid.addWidget(btn, row, col)
                self.tombol_map[teks] = btn

        # ====== Gabungkan Grid dengan VBox ======
        vbox = QVBoxLayout()
        vbox.addWidget(self.output)
        vbox.addLayout(grid)
        self.calc_tab.setLayout(vbox)

        # ====== Riwayat ======
        self.history_list = QListWidget()
        layout_history = QVBoxLayout()
        layout_history.addWidget(QLabel("Riwayat Perhitungan:"))
        layout_history.addWidget(self.history_list)
        self.history_tab.setLayout(layout_history)

        # ====== Sinyal Tombol ======
        angka = ["0", "1", "2", "3", "4", "6", "8", "9"]
        operasi = ["+", "-", "*", "/", "."]

        for a in angka:
            self.tombol_map[a].clicked.connect(self.pushBut)
        for o in operasi:
            self.tombol_map[o].clicked.connect(self.pushBut)

        self.tombol_map["="].clicked.connect(self.pushBut)
        self.tombol_map["CN"].clicked.connect(self.clear_output)
        self.tombol_map["DEL"].clicked.connect(self.delete_last)

        # ====== Menu Bar ======
        self.create_menu()

    # ====== Fungsi Menu ======
    def create_menu(self):
        menuBar = self.menuBar()
        file_menu = menuBar.addMenu("File")
        exit_action = QAction("Keluar", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    # ====== Fungsi Kalkulator ======
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