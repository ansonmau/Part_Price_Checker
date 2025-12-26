from PySide6.QtCore import Qt, Slot, Signal, QObject
from PySide6.QtGui import QFont, QInputDevice
from PySide6.QtWidgets import (
    QApplication, QGroupBox, QInputDialog, QLineEdit, QMainWindow, QProgressBar, QPushButton, QStatusBar, QStyleOptionProgressBar, QTableWidget, QTextBrowser, QTextEdit, QVBoxLayout, QWidget, QPlainTextEdit, QHBoxLayout, QDialog,
    QLabel,
     )

from scripts.misc.Thread import Thread, Worker
from scripts.web.Manager import Manager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.web_manager = Manager([])

        self.setWindowTitle("Price Part Checker 1.0.0")
        self.resize(300, 650)

        self.cen_layout = QVBoxLayout()
        self.cen_widget = QWidget()
        self.cen_widget.setLayout(self.cen_layout)
        self.setCentralWidget(self.cen_widget)

        self.init_central_layout()
        self.init_widget_functionality()


    @Slot()
    def init_central_layout(self):
        top_wig = QWidget()
        top_lay = QHBoxLayout()
        top_wig.setLayout(top_lay)

        mid_wig = QWidget()
        mid_lay = QHBoxLayout()
        mid_wig.setLayout(mid_lay)

        bot_wig = QWidget()
        bot_lay = QVBoxLayout()
        bot_wig.setLayout(bot_lay)

        self.cen_layout.addWidget(top_wig)
        self.cen_layout.addWidget(mid_wig)
        self.cen_layout.addWidget(bot_wig)

        self.settings_btn = QPushButton("Settings")
        self.server_btn = QPushButton("Server")
        self.search_btn = QPushButton("Search")
        self.id_input = QLineEdit()
        self.progress_bar = QProgressBar()
        self.results_area = QTableWidget()

        top_lay.addWidget(self.settings_btn)
        top_lay.addWidget(self.server_btn)

        mid_lay.addWidget(self.id_input)
        mid_lay.addWidget(self.search_btn)

        bot_lay.addWidget(self.progress_bar)
        bot_lay.addWidget(self.results_area)

    def init_widget_functionality(self):
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(40)

        self.search_btn.clicked.connect(self.run_manager_on_new_thread)


    def run_manager_on_new_thread(self):
        self.worker = Worker()
        self.worker.set_exec_fnc(self.web_manager.run)
        self.w_thread = Thread()
        self.w_thread.attach_worker(self.worker)


    @Slot()
    def set_progress(self, val: int):
        self.progress_bar.setValue(val)

    
