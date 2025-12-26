from PySide6.QtWidgets import QApplication
from scripts.misc.Log import disable_noisy_libs_logs
import scripts.qb.Parser as parser
from scripts.misc.Utils import ROOT
from scripts.ui.Main_Window import MainWindow

def manager_test():
    from scripts.web.Manager import Manager
    m = Manager()
    m.scrape_price("ST10000VE001")

def newegg_test():
    from scripts.web.sources.NewEgg import NewEgg
    NE = NewEgg()
    NE.scrape_price("WDS200T2R0A")

def cc_test():
    from scripts.web.sources.CanadaComputers import CanadaComputers
    CC = CanadaComputers()
    price = CC.scrape_price("Prime RTX-5080-O16G")

def main():
    qb_file = ROOT / "data" / "qb.xlsx"
    parser.parse(qb_file)

    app = QApplication()
    window = MainWindow() 
    window.show()
    app.exec()

if __name__ == "__main__":
    disable_noisy_libs_logs()
    manager_test()

