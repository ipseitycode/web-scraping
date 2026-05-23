class Configuration:
    def __init__(self):
        self.__base_url = "https://lista.mercadolivre.com.br"
        self.__client_type = "playwright"
        self.__user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
        self.__viewport = {"width": 1366, "height": 768}
        self.__locale = "pt-BR"
        self.__timezone = "America/Sao_Paulo"
        self.__launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
        # NUMERO MAXIMO DE ITENS POR SCRAPER
        self.__max_items = 500

    def setupBaseUrl(self):
        return self.__base_url

    def setupMaxItems(self):
        return self.__max_items

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
