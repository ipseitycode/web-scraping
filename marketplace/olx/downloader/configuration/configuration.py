from marketplace.olx.shared.config.settings import HTTP_TIMEOUT_SECONDS

class Configuration:
    def __init__(self):
        self.__base_url = "https://www.olx.com.br"
        self.__client_type = "playwright"
        self.__user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        self.__viewport = {"width": 1366, "height": 768}
        self.__locale = "pt-BR"
        self.__timezone = "America/Sao_Paulo"
        self.__launch_args = ["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"]
        self.__max_items = 200
        self.__timeout_seconds = HTTP_TIMEOUT_SECONDS

    def setupBaseUrl(self):
        return self.__base_url

    def setupClientType(self):
        return self.__client_type

    def setupUserAgent(self):
        return self.__user_agent

    def setupViewport(self):
        return self.__viewport

    def setupLocale(self):
        return self.__locale

    def setupTimezone(self):
        return self.__timezone

    def setupLaunchArgs(self):
        return self.__launch_args

    def setupMaxItems(self):
        return self.__max_items

    def setupTimeout(self):
        return self.__timeout_seconds
