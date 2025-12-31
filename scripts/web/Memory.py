from scripts.misc.Utils import ROOT
import json


class Memory():
    memory_file = ROOT / "data" / "item_memory.json"

    def __init__(self) -> None:
        self.memory = {}
        self.last_key = None

    def load_from_file(self):
        with open(self.memory_file, 'r') as f:
            self.memory = json.load(f)
            self.last_key = list(self.memory.keys())[-1]
        
    def find(self, item_id):
        return self.memory.get(item_id)

    def save_to_file(self):
        key_list = list(self.memory.keys())[-1]
        last_index = key_list.find(self.last_key)

        


