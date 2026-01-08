from PySide6.QtWidgets import QApplication
from scripts.misc.Log import disable_noisy_libs_logs
import scripts.qb.Parser as parser
from scripts.misc.Utils import ROOT
from scripts.ui.Main_Window import MainWindow
import scripts.misc.Init as Init

def manager_test():
    from scripts.web.Manager import Manager
    m = Manager()
    m.scrape_price("i9-14900KF")

def cc_test():
    from scripts.web.sources.CanadaComputers import CanadaComputers
    CC = CanadaComputers()
    p = CC.scrape_price("CMT32GX5M2X6000C36")
    print(f'Price found: {p}')
    p = CC.scrape_price("B850M EAGLE WF6E")
    print(f'Price found: {p}')
    p = CC.scrape_price("i9-14900KF")
    print(f'Price found: {p}')
    p = CC.scrape_price("MAG CORELIQUID E360 WHITE")
    print(f'Price found: {p}')

def me_test():
    from scripts.web.sources.MemoryExpress import MemoryExpress
    ME = MemoryExpress()
    price = ME.scrape_price("CMT32GX5M2X6000C36")
    # price = ME.scrape_price("B850M EAGLE WF6E")
    # price = ME.scrape_price("i9-14900KF")
    # price = ME.scrape_price("MAG CORELIQUID E360 WHITE")

def memory_test():
    from scripts.web.Memory import Memory 
    M = Memory('CC')
    M.add('test', 'test_model_name')
    M.save_to_file()

    M2=Memory('NE')
    M2=Memory('NE')

def main():
    qb_file = ROOT / "data" / "qb.xlsx"
    parser.parse(qb_file)

    app = QApplication()
    window = MainWindow() 
    window.show()
    app.exec()

if __name__ == "__main__":
    Init.init()
    disable_noisy_libs_logs()
    cc_test()
