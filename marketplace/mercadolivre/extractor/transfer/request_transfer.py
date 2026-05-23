class RequestTransfer:
    def __init__(self):
        self.__title = None
        self.__price = None
        self.__url = None
        self.__rating = None
        self.__price_original = None
        self.__installments = None
        self.__shipping = None
        self.__seller = None

    def getTitle(self): return self.__title
    def setTitle(self, title: str): self.__title = title

    def getPrice(self): return self.__price
    def setPrice(self, price: str): self.__price = price

    def getUrl(self): return self.__url
    def setUrl(self, url: str): self.__url = url

    def getRating(self): return self.__rating
    def setRating(self, rating: str): self.__rating = rating

    def getPriceOriginal(self): return self.__price_original
    def setPriceOriginal(self, price_original: str): self.__price_original = price_original

    def getInstallments(self): return self.__installments
    def setInstallments(self, installments: str): self.__installments = installments

    def getShipping(self): return self.__shipping
    def setShipping(self, shipping: str): self.__shipping = shipping

    def getSeller(self): return self.__seller
    def setSeller(self, seller: str): self.__seller = seller
