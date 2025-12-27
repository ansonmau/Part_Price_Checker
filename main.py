from PySide6.QtWidgets import QApplication
from scripts.misc.Log import disable_noisy_libs_logs
import scripts.qb.Parser as parser
from scripts.misc.Utils import ROOT
from scripts.ui.Main_Window import MainWindow

def manager_test():
    from scripts.web.Manager import Manager
    m = Manager()
    m.scrape_price("i9-14900KF")

def me_test():
    from scripts.web.sources.MemoryExpress import MemoryExpress
    ME = MemoryExpress()
    ME.scrape_price("")


def main():
    qb_file = ROOT / "data" / "qb.xlsx"
    parser.parse(qb_file)

    app = QApplication()
    window = MainWindow() 
    window.show()
    app.exec()

if __name__ == "__main__":
    disable_noisy_libs_logs()
    me_test()
