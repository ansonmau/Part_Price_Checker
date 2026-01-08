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
    me_test()
