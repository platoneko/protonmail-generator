import time
import settings
from utils.temporary_email_services.abstract_email import Mail
from utils.temporary_email_services.api_classes.MailApis.maildrop_api import MailDropApi

class MailDrop(MailDropApi, Mail):
    def __init__(self, mailbox, subject_name, tries_to_stop, sleeping_time):
        super().__init__(mailbox, subject_name, tries_to_stop, sleeping_time)

    def get_code_by_many_tries(self):
        verification_code = None
        tries = 0

        while not verification_code:
            if tries >= settings.tries_count:
                return None
            else:
                verification_code = self.__get_code()
                tries += 1
                if not verification_code:
                    time.sleep(self.__sleeping_time)
        return verification_code
