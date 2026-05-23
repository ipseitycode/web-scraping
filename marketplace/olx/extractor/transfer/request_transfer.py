class RequestTransfer:
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
    def setTitle(self, title): self.__title = title

    def getPrice(self): return self.__price
    def setPrice(self, price): self.__price = price

    def getUrl(self): return self.__url
    def setUrl(self, url): self.__url = url

    def getLocation(self): return self.__location
    def setLocation(self, location): self.__location = location

    def getDate(self): return self.__date
    def setDate(self, date): self.__date = date

    def getImage(self): return self.__image
    def setImage(self, image): self.__image = image

    def getInstallments(self): return self.__installments
    def setInstallments(self, installments): self.__installments = installments

    def getBadges(self): return self.__badges
    def setBadges(self, badges): self.__badges = badges

    def getImageCount(self): return self.__image_count
    def setImageCount(self, image_count): self.__image_count = image_count
