from PySide6.QtCore import Qt, Slot, Signal, QObject

from scripts.qb.Item import Item
from scripts.misc.Settings import Settings
from scripts.misc.Log import MyLogger

from scripts.web.sources.NewEgg import NewEgg
from scripts.web.sources.CanadaComputers import CanadaComputers
from scripts.web.sources.MemoryExpress import MemoryExpress

logger = MyLogger("WebManager")

class Manager():
    progress = Signal()
    finished = Signal()

    def __init__(self):
        self.settings = Settings()
        self.settings.load_from_file()
        self.NE = NewEgg()
        self.CC = CanadaComputers()
        self.ME = MemoryExpress()
    
    def scrape_price(self, item_id):
        CC_price = self.CC.scrape_price(item_id)
        NE_price = self.NE.scrape_price(item_id)
        ME_price = self.ME.scrape_price(item_id)

        logger.debug("Canada Computers: {}".format(CC_price))
        logger.debug("NewEgg: {}".format(NE_price))
        logger.debug("Memory Express: {}".format(ME_price))
    
