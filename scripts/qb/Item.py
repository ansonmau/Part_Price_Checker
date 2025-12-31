from scripts.misc.Log import MyLogger


logger = MyLogger("Item_Module")

class Item:
    sources = ["cc", "az", "ne", "me"]
    def __init__(self):
        self.new_price = -1
        self.paid = -1
        self.id = ""
        self.qty = 0
        self.source = "NA"

    def set_source(self, source):
        conversion = {
            "canada": "cc",
            "newegg": "ne",
            "amazon": "az",
            "memory": "me"
        }

        for source_name_abr in conversion:
            if source_name_abr in source:
                self.source = conversion[source_name_abr]
                return

        logger.debug("Failed to convert source name \"{}\"".format(source))

    def set_new_price(self, price):
        self.new_price = price 

    def set_paid(self, price):
        self.paid = price 

    def set_id(self, id):
        self.id = id

    def set_qty(self, qty):
        self.qty = qty

    def set_open_box(self, val: bool):
        self.open_box = val

    def get_source(self):
        return self.source

    def get_id(self):
        return self.id

    def get_qty(self):
        return self.qty

    def get_new_price(self):
        return self.new_price 

    def get_paid_price(self):
        return self.paid

