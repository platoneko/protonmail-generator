from utils.temporary_email_services.email_services import services
from utils.exceptions import NotAvailableDomainException, GettingVerificationCodeException
import settings


class EmailBox:
    def __init__(self):
        self.__gen = self.__domains_gen()
        self.__email_class = None
        self.__email_domain = None


    @staticmethod
    def __domains_gen():
        for service in services:
            yield service.class_of_service, service.domain_name

    def get_another_domain(self):
        try:
            self.__email_class, self.__email_domain = next(self.__gen)
        except StopIteration:
            raise NotAvailableDomainException('No more email domains available')

    @property
    def email_class(self):
        return self.__email_class

    @property
    def email_domain(self):
        return self.__email_domain

    def get_verification_code(self, username):
        box = self.__email_class(mailbox=username, subject_name="Proton Verification Code",
                                 tries_to_stop=settings.tries_count, sleeping_time=settings.min_time_to_sleep)
        try:
            result = box.get_code_by_many_tries()
            return result
        except Exception:
            raise GettingVerificationCodeException(f'No code was received!')

