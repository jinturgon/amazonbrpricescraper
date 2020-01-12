class Product:
    def __init__(self, name, price, prevPrice, discount, link):
        self.name = name
        self.price = price
        self.prevPrice = prevPrice
        self.discount = discount
        self.link = link
    
    def serialize(self):
        return {
            "name" : self.name,
            "price" : self.price,
            "prevPrice" : self.prevPrice,
            "discount" : str(self.discount) + " %",
            "link" : self.link
        }
    
    def from_json(self, json_):
        self.name = json_["name"]
        self.price = json_["price"]
        self.prev_price = json_["prevPrice"]
        self.discount = json_["discount"]
        self.link = json_["link"]