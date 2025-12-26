import re
from scripts.qb.Item import Item
from scripts.misc.Utils import ROOT
import pandas as pd 
from scripts.misc.Log import MyLogger

logger = MyLogger("QB_Parser")

def parse(qb_xlsx_file):
    qb = pd.read_excel(qb_xlsx_file, sheet_name="Sheet1")

    valid_sources = ["canada computers", "amazon", "newegg", "memory express"]
    pattern = "|".join(valid_sources)
    valid_rows = qb[qb["Source Name"].str.contains(pattern, case=False, na=False)]

    items = []
    for i, row in valid_rows.iterrows():
        if check_row_is_valid(row):
            items.append(convert_row_to_item(row))

    seen = set()
    with open(ROOT / "out.txt", 'w') as f:
        for c in items:
            if c.id not in seen:
                # f.write("{} {} {}\n".format(c.id, c.qty, c.paid))
                f.write("{} ({})\n".format(c.id, c.source))
                seen.add(c.id)


def check_row_is_valid(row) -> bool:
    if "shipping charges" in row["Item"].lower():
        return False
    if row["Item"].lower() == "cable":
        return False
    if row["Qty"] < 0:
        return False

    return True

def convert_row_to_item(row) -> Item:
    curr = Item()
    if "open box" in row["Item"].lower():
        curr.set_open_box(True)
    curr.set_id(parse_item_name(row["Item"]))
    curr.set_qty(row["Qty"])
    curr.set_paid(row["Cost Price"])
    curr.set_source(parse_source_name(row["Source Name"]))
    
    return curr

def parse_item_name(full_item_name) -> str:
    sku = full_item_name
    try:
        left, right = full_item_name.split("(", 1)
        sku = left.split(':')[-1]
    except:
        logger.debug("Failed to parse item name: {}".format(full_item_name))

    return sku

def parse_source_name(full_source_name) -> str:
    pattern = r"^\s*([^(]+?)\s*(?:\(|$)"
    source = re.search(pattern, full_source_name)
    return source.group(1)
