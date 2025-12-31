from scripts.misc.Utils import ROOT
import json


class Memory():
    memory_file = ROOT / "data" / "item_memory.json"

    def __init__(self, source) -> None:
        self.source = source
        self.memory = {}

    def find(self, item_id: str) -> str | None:
        return self.memory.get(item_id)

    def add(self, item_id: str, mem_id: str) -> None:
        self.memory[item_id] = mem_id

    def load_from_file(self) -> None:
        with open(self.memory_file, 'r') as f:
            self.memory = json.load(f)[self.source]
        
    def save_to_file(self):
        with open(self.memory_file, 'r') as f:
            d = json.load(f)
        d[self.source] = self.memory

        with open(self.memory_file, 'w') as f:
            json.dump(d, f)

    def reset(self):
        self.memory = {}
        self.save_to_file()

        


