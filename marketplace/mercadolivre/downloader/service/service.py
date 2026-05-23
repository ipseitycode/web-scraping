import time
from playwright.sync_api import sync_playwright, TimeoutError
from shared.base.base_downloader import BaseDownloader
from marketplace.mercadolivre.shared.config import settings as module_settings
from marketplace.mercadolivre.downloader.configuration.configuration import Configuration
from marketplace.mercadolivre.downloader.validator.validator import Validator
from marketplace.mercadolivre.downloader.transfer.request_transfer import RequestTransfer

class Service(BaseDownloader):
    def __init__(self):
        super().__init__(
            retry_attempts=module_settings.HTTP_RETRY_ATTEMPTS,
            delay_seconds=module_settings.HTTP_DELAY_SECONDS,
        )
        self.__config = Configuration()
        self.__validator = Validator()

    def _fetch(self, request: RequestTransfer):
        query = request.getQuery().replace(' ', '-')
        base_url = self.__config.setupBaseUrl()
        client_type = self.__config.setupClientType()
        max_items = self.__config.setupMaxItems()
        html_pages = []

        if client_type == "playwright":
            timeout_ms = module_settings.HTTP_TIMEOUT_SECONDS * 1000
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=self.__config.setupLaunchArgs()
                )
                context = browser.new_context(
                    user_agent=self.__config.setupUserAgent(),
                    viewport=self.__config.setupViewport(),
                    locale=self.__config.setupLocale(),
                    timezone_id=self.__config.setupTimezone(),
                    extra_http_headers={"Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"},
                )
                page = context.new_page()
                page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

                offset = 1
                is_first_page = True

                while True:
                    if is_first_page:
                        url = f"{base_url}/{query}_NoIndex_True"
                    else:
                        url = f"{base_url}/{query}_Desde_{offset}_NoIndex_True"

                    page.goto(url, timeout=timeout_ms)

                    try:
                        page.wait_for_selector('a.poly-component__title', timeout=timeout_ms)
                    except TimeoutError:
                        break

                    html = page.content()
                    html_pages.append(html)

                    if len(html_pages) * 48 >= max_items:
                        break

                    if is_first_page:
                        offset = 49
                        is_first_page = False
                    else:
                        offset += 48

                    time.sleep(module_settings.HTTP_DELAY_SECONDS)

                context.close()
                browser.close()

        self.__validator.validateResponse(html_pages)
        return html_pages
