from patchright.sync_api import sync_playwright, Playwright
from utils.common.userdata import UserData
import json
import time
from utils.tor.tor_proc import TorProcess
import settings


class BasePlaywright:
    def __init__(self):
        self.headless = not settings.show_browser_window
        self.browser = None
        self.context = None
        self.page = None
        self.user_data = UserData()
        self.proxy_server = settings.tor_proxy_path if settings.use_tor else None
        self.playwright: Playwright = None
        self.tor_proc = TorProcess()
        self.session_started = False
        self.current_ip = None

    def start_session(self):
        if not self.session_started:
            try:
                self.playwright: Playwright = sync_playwright().start()
                proxy_config = {"server": self.proxy_server} if settings.use_tor else None

                # device = self.playwright.devices['iPad Mini']
                self.browser = self.playwright.chromium.launch(
                    # executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",
                    headless=self.headless,
                    args=["--start-maximized"],
                    proxy=proxy_config
                )
                self.generate_context_and_page()
                self.session_started = True
                settings.logger.info("Session started successfully")
            except Exception as e:
                raise ValueError(f"Error during session initialization: {e}")

    def generate_context_and_page(self):
        self.user_data.generate_user_agent()
        self.user_data.generate_timezone()

        self.context = self.browser.new_context(
            # **device,
            no_viewport=True,
            user_agent=self.user_data.user_agent,
            locale="en-US",
            timezone_id=self.user_data.timezone,
            # device_scale_factor=3,
            # is_mobile=True,
            # has_touch=True,
            viewport=self.user_data.viewport,
            color_scheme="dark"
        )
        self.page = self.context.new_page()
        self.page.set_default_timeout(settings.max_playwright_waiting_time)  # Seconds
        self.page.set_default_navigation_timeout(settings.max_playwright_waiting_time)  # Navigation

    def go_to(self, url: str, timeout: int = settings.max_timeout):
        try:
            self.page.goto(url, timeout=timeout)
            self.page.wait_for_load_state('domcontentloaded', timeout=timeout)
            settings.logger.info(f'The script accessed the website: {url}')
            time.sleep(settings.min_time_to_sleep)
        except Exception as e:
            raise ValueError(f"Failed to navigate to {url}: {e}")

    def close_session(self):
        if self.session_started:
            try:
                self.page.close()
                self.context.close()
                self.browser.close()
                self.playwright.stop()
                self.session_started = False
            except Exception as e:
                settings.logger.error(f"Error during session cleanup: {e}")
                # print(f"Error during session cleanup: {e}")

    def get_current_ip(self, timeout: int = settings.min_timeout):
        try:
            self.page.goto("https://api.ipify.org?format=json", timeout=timeout)
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            self.current_ip = json.loads(self.page.inner_text("body"))
        except Exception as e:
            self.current_ip = {'ip': 'Failed to get IP'}
