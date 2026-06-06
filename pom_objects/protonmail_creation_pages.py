import time
import random
from utils.exceptions import EmailMethodForVerificationDisabled, GettingVerificationCodeException, SkipAdvIncomplete
from pom_objects.base_playwright import BasePlaywright
import settings


def human_delay(low=1.5, high=4.0):
    time.sleep(random.uniform(low, high))


class ProtonmailCreationPages(BasePlaywright):
    def __init__(self):
        super().__init__()
        self.is_mobile = False

    def __set_user_data(self):
        self.page.locator(
            "iframe[title=\"Email address\"]").content_frame.get_by_test_id(
            "input-input-element").type(
            self.user_data.nickname, delay=random.randint(80, 200))

        human_delay()
        self.page.get_by_role("textbox", name="Password").type(
            self.user_data.password, delay=random.randint(60, 150))

        human_delay()
        if not self.is_mobile:
            self.page.get_by_placeholder("Confirm password").type(
                self.user_data.password, delay=random.randint(60, 150))
        else:
            self.page.get_by_role("textbox", name="Confirm password").type(
                self.user_data.password, delay=random.randint(60, 150))
        human_delay(2, 5)

    def __create_account_button_click(self):
        human_delay(2, 4)
        self.page.get_by_role("button", name="Start using Proton Mail now").click()
        settings.logger.info("Filling out the fields on the registration page")
        human_delay(1.5, 3)
        self.page.get_by_role("button", name="No, thanks").click()
        human_delay(2, 5)

    def __try_register_using_temp_mail(self):
        settings.logger.info("Finding email button and field...")
        input("[DEBUG] 验证页面已加载，请截图发给我，然后按回车继续...")
        try:
            button = self.page.get_by_test_id("tab-header-email-button")
            if button.is_visible():
                button.click()
            else:
                settings.logger.info("Email method is already changed!")
                return
            time.sleep(settings.min_time_to_sleep)

            self.page.get_by_test_id(
                "verification"
            ).get_by_test_id(
                "input-input-element"
            ).fill(
                self.user_data.full_email_name_for_verification)
        except Exception:
            raise EmailMethodForVerificationDisabled(
                'Verification by email is not available now! Please try again later or use vpn.')

        self.page.get_by_role("button", name="Get verification code").click()
        time.sleep(settings.min_time_to_sleep)
        alert = self.page.get_by_role('alert').inner_text()
        return alert

    def __register_with_temporary_email(self):
        settings.logger.info("Trying to register using temporary email")
        alert = self.__try_register_using_temp_mail()
        if alert is None:
            return
        if 'Please wait a few minutes' in alert:
            time.sleep(settings.time_to_sleep_waiting_for_request)
            self.page.get_by_role("button", name="Get verification code").click()
        else:
            while ('Email address verification temporarily disabled for this email domain. '
                   'Please try another verification method') in alert:
                settings.logger.info(f"Email domain {self.user_data.email_domain} is not enable for verification now!")
                self.user_data.get_another_domain()
                alert = self.__try_register_using_temp_mail()

    def __insert_verification_code(self):
        while True:
            settings.logger.info("Trying to find a verification code")
            try:
                code = self.user_data.verification_code
                if code:
                    settings.logger.info(f"Verification code: {code}")
                    break
            except GettingVerificationCodeException:
                settings.logger.info(f'{self.user_data.email_domain} domain is not working now...')
                self.user_data.get_another_domain()
                self.page.get_by_role("button", name="Resend code").click()
                self.page.get_by_role("button", name="Edit email address").click()

                self.__register_with_temporary_email()

        self.page.get_by_test_id("verification").get_by_test_id("input-input-element").fill(code)
        time.sleep(settings.two_seconds)
        self.page.get_by_role("button", name="Verify").click()

    def __skip_adv(self):
        try:
            main_lst = (
                self.page.get_by_role("button", name="Get started"),
                self.page.get_by_role("button", name="Select theme"),
                self.page.get_by_role("button", name="Install later"),
                self.page.get_by_role("button", name="Continue"),
                self.page.get_by_role("button", name="Skip for now")
            )
            for button in main_lst:
                time.sleep(settings.two_seconds)
                button.click()
        except SkipAdvIncomplete:
            raise SkipAdvIncomplete("Skip adv buttons is not visible!")

    def __finishing_registration(self):
        settings.logger.info("Finishing registration...")
        button = self.page.get_by_role("button", name="Continue")
        if button.is_enabled():
            button.click()
        else:
            raise ValueError("Skip adv button is not visible!")
        self.page.get_by_role("button", name="Maybe later").click()
        self.page.get_by_role("button", name="Confirm").click()

    def set_recovery_address(self):
        self.page.get_by_test_id("settings-drawer-app-button:settings-icon").click()
        self.page.get_by_test_id("drawer-quick-settings:all-settings-button").click()
        self.page.get_by_role("link", name="Recovery Attention required").click()
        time.sleep(settings.min_time_to_sleep)
        # Set email
        self.page.get_by_role("textbox", name="Recovery email address").fill(self.user_data.recovery_email.email)
        self.page.get_by_test_id('account:recovery:emailSubmit').click()
        self.page.get_by_role("textbox", name="Password").fill(self.user_data.password)
        self.page.get_by_role("button", name="Authenticate").click()
        time.sleep(settings.min_time_to_sleep)
        self.page.get_by_role("button", name="Verify now this recovery").click()
        self.page.get_by_role("button", name="Verify with email").click()
        time.sleep(settings.min_time_to_sleep)
        self.page.get_by_text("Verification email sent to").click()

        try:
            self.page.get_by_text(f"Verification email sent to {self.user_data.recovery_email.email}")
            settings.logger.info("Verification email was sent!")
        except:
            raise ValueError("Verification email was not sent!")

    def __signing_function(self, email, password):
        self.page.get_by_role("textbox", name="Email or username").fill(email)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()

    def login_to_account(self, email, password):
        self.go_to(settings.protonmail_login_address)
        self.__signing_function(email, password)
        self.page.get_by_test_id("explore-drive").click()
        try:
            self.__skip_adv()
        except Exception:
            settings.logger.info("No need to skip adv!")

    def run_registration(self):
        self.go_to(settings.protonmail_registration_address)
        button = self.page.get_by_role("button", name="create a new account")
        if button.is_visible():
            button.click()
        self.__set_user_data()
        self.__create_account_button_click()
        self.__register_with_temporary_email()
        self.__insert_verification_code()
        time.sleep(settings.min_time_to_sleep)
        self.__finishing_registration()
        time.sleep(settings.min_time_to_sleep)
        self.page.get_by_test_id("explore-drive").click()
        self.__skip_adv()
