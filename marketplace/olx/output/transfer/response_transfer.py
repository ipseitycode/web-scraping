class ResponseTransfer:
    def __init__(self):
        self.__title = None
        self.__price = None
        self.__url = None
        self.__location = None
        self.__date = None
        self.__image = None
        self.__installments = None
        self.__badges = None
        self.__image_count = None

    def getTitle(self): return self.__title
    def setTitle(self, title: str): self.__title = title

    def getPrice(self): return self.__price
    def setPrice(self, price: str): self.__price = price

    def getUrl(self): return self.__url
    def setUrl(self, url: str): self.__url = url

    def getLocation(self): return self.__location
    def setLocation(self, location: str): self.__location = location

    def getDate(self): return self.__date
    def setDate(self, date: str): self.__date = date

    def getImage(self): return self.__image
    def setImage(self, image: str): self.__image = image

    def getInstallments(self): return self.__installments
    def setInstallments(self, installments: str): self.__installments = installments

    def getBadges(self): return self.__badges
    def setBadges(self, badges: list): self.__badges = badges

    def getImageCount(self): return self.__image_count
    def setImageCount(self, image_count: int): self.__image_count = image_count

    def toJson(self) -> dict:
        return {
            "title": self.__title,
            "price": self.__price,
            "url": self.__url,
            "location": self.__location,
            "date": self.__date,
            "image": self.__image,
            "installments": self.__installments,
            "badges": self.__badges,
            "image_count": self.__image_count
        }
