import re
import requests

class MemoryExpress:
    def __init__(self):
        pass

    def scrape_price(self, item_id):
        url = "https://www.newegg.ca/p/pl?d=F5-6000J3636F16GX2-FX5"
        print(requests.get(url).text)


    def _extract_price(self, price_text) -> float:
        search_pattern = r"Only\$(\d+(?:,\d{3})*\.\d{2})"

        search = re.search(search_pattern, price_text)
        if search:
            price = search.group(1)
            price = float(price.replace(',', ''))
        else:
            price = float(-1)

        return price
    
