import time
import datetime
import settings
from pom_objects.protonmail_creation_pages import ProtonmailCreationPages
from utils import exceptions
from utils.registration_authenticate.submit_adding_mail import submit_adding_mail
from utils.recovery_email import EmailData


class App(ProtonmailCreationPages):
    def __init__(self):
        super().__init__()
        self.__account_count = 0
        self.__tries = 0
        self.__status = None

    def create_multiple_accounts(self, accounts_count: int):
        try:
            self.user_data.get_another_domain()

            if settings.use_tor:
                self.tor_proc.start_tor_background()

            for ind in range(1, accounts_count + 1):
                print(f"Creating {ind} account")

                if ind == accounts_count:
                    self.__status = 'last'
                elif ind == 1:
                    self.__status = 'first'
                else:
                    self.__status = 'middle'

                yield from self.__try_to_create_account(ind)

        finally:
            if settings.use_tor:
                self.tor_proc.terminate()
                self.close_session()

    def __try_to_create_account(self, ind):
        while True:
            try:
                self.__create_account()
                self.close_session()
                break
            except exceptions.SkipAdvIncomplete as exc:
                email, password = self.user_data.proton_email_and_proton_password
                raise exceptions.SkipAdvIncomplete(
                    f"Account:\nEmail:\n{email}"
                    f"\nPassword:\n{password}"
                    f"\nCreated, but adv was not skipped...")

            except exceptions.GettingVerificationCodeException as exc:
                raise exceptions.GettingVerificationCodeException(
                    f"Failed to create account!\n"
                    f"Temporary email was not sent email...\n"
                    f"Current email number: {ind}\n"
                    f"Exception describe: {exc}")
            except exceptions.EmailMethodForVerificationDisabled as exc:
                settings.logger.info(f'Email method is not available in this session...\n{exc}')
            except (exceptions.NotAvailableDomainException,
                    exceptions.RecoveryEmailProblemException,
                    exceptions.VerifyException) as exc:
                raise exc(f'Problem with registration account {ind}'
                          f'\n{exc}')

            except Exception as exc:
                self.close_session()
                settings.logger.error(f"Failed to create account {ind}\n{exc}")
                self.__tries += 1
                if self.__tries <= settings.tries_count_registration:
                    settings.logger.error(f"Try {self.__tries} of {settings.tries_count_registration}\n{exc}")
                    self.tor_proc.restart_tor_process()
                else:
                    if self.__account_count >= 2:
                        self.__verify_first_account(self.user_data.last_email.email, self.user_data.last_email.password)
                        settings.logger.info('Accounts verified')
            finally:
                self.close_session()

        email, password = self.user_data.proton_email_and_proton_password
        yield email, password, datetime.datetime.now().strftime(settings.time_format), self.current_ip['ip']


    def __check_ip(self):
        self.get_current_ip()
        if self.current_ip['ip'] is not None:
            settings.logger.info(f"Current IP: {self.current_ip['ip']}")

    def __create_account(self):
        self.user_data.generate_new_user()
        self.start_session()

        if settings.use_tor:
            self.__check_ip()

        self.run_registration()
        protonmail_login, protonmail_password = self.user_data.proton_email_and_proton_password

        if self.__status == 'first':
            self.user_data.recovery_email = EmailData(protonmail_login, protonmail_password)
            settings.logger.info('This address has been added for recovery others')

        elif self.__status == 'last':
            self.__verify()
            self.__verify_first_account(protonmail_login, protonmail_password)
        else:
            self.__verify()
        self.__account_count += 1
        self.user_data.last_email = EmailData(protonmail_login, protonmail_password)

    def __get_verify_link(self):
        login, password = self.user_data.recovery_email.email, self.user_data.recovery_email.password
        verify_link = submit_adding_mail(login, password)
        return verify_link

    def __verify(self):
        self.set_recovery_address()
        self.close_session()
        settings.logger.info('Waiting for verification...')
        time.sleep(settings.max_time_to_sleep)
        link = self.__get_verify_link()
        self.start_session()
        self.page.goto(link)
        time.sleep(settings.min_time_to_sleep)

        locator = self.page.get_by_role("heading", name="Email verified")
        if not locator.is_visible():
            raise exceptions.RecoveryEmailProblemException("Recovery  email was not added!")
        settings.logger.info(f"Email: {self.user_data.proton_email_and_proton_password[0]} was verified successfully!")

    def __verify_first_account(self, protonmail_login, protonmail_password):
        last_recovery_mail = self.user_data.recovery_email
        try:
            current_password = None
            self.login_to_account(email=self.user_data.recovery_email.email,
                                  password=self.user_data.recovery_email.password)
            self.user_data.recovery_email = EmailData(protonmail_login, protonmail_password)
            current_password = self.user_data.password
            self.user_data.password = last_recovery_mail.password
            self.__verify()
            settings.logger.info('All accounts verified!')
            self.user_data.password = current_password
        except Exception as exc:
            raise exceptions.VerifyException(f"Failed to login to {protonmail_login} | {exc}")
