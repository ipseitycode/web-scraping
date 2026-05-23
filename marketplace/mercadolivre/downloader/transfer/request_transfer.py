class RequestTransfer:
    def __init__(self):
        self.__query = None
        self.__domain = None
        self.__target = None
        self.__filters = {}

    def getQuery(self): return self.__query
    def setQuery(self, query: str): self.__query = query

    def getDomain(self): return self.__domain
    def setDomain(self, domain: str): self.__domain = domain

    def getTarget(self): return self.__target
    def setTarget(self, target: str): self.__target = target

    def getFilters(self): return self.__filters
    def setFilters(self, filters: dict): self.__filters = filters
