import time
from playwright.sync_api import sync_playwright
from shared.base.base_downloader import BaseDownloader
from marketplace.olx.downloader.configuration.configuration import Configuration
from marketplace.olx.downloader.validator.validator import Validator
from marketplace.olx.shared.config.settings import HTTP_RETRY_ATTEMPTS, HTTP_DELAY_SECONDS

class Service(BaseDownloader):
    def __init__(self):
        super().__init__(retry_attempts=HTTP_RETRY_ATTEMPTS, delay_seconds=HTTP_DELAY_SECONDS)
        self.__config = Configuration()
        self.__validator = Validator()

    def _fetch(self, request):
        base_url = self.__config.setupBaseUrl()
        user_agent = self.__config.setupUserAgent()
        viewport = self.__config.setupViewport()
        locale = self.__config.setupLocale()
        timezone = self.__config.setupTimezone()
        launch_args = self.__config.setupLaunchArgs()
        max_items = self.__config.setupMaxItems()
        timeout_ms = self.__config.setupTimeout() * 1000

        estado = request.getEstado() if request.getEstado() else "brasil"
        query = request.getQuery()

        raw_contents = []
        page_num = 1
        items_collected = 0

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=launch_args
            )
            
            context = browser.new_context(
                user_agent=user_agent,
                viewport=viewport,
                locale=locale,
                timezone_id=timezone
            )
            
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            page = context.new_page()

            while items_collected < max_items:
                if page_num == 1:
                    url = f"{base_url}/{estado}?q={query}"
                else:
                    url = f"{base_url}/{estado}?q={query}&o={page_num}"

                try:
                    page.goto(url, timeout=timeout_ms)
                    page.wait_for_selector('section.olx-adcard', timeout=timeout_ms)
                except Exception:
                    break

                html = page.content()
                raw_contents.append(html)
                
                cards_count = page.locator('section.olx-adcard').count()
                if cards_count == 0:
                    break
                    
                items_collected += cards_count
                page_num += 1
                
                time.sleep(HTTP_DELAY_SECONDS)

            browser.close()

        self.__validator.validateResponse(raw_contents, request.getDomain(), request.getTarget())
        return raw_contents
