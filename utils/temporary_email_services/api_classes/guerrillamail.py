import re
from time import sleep

from utils.temporary_email_services.abstract_email import Mail
from utils.temporary_email_services.api_classes.MailApis.guerrilla_api import GuerrillaMailSession


class GuerrillaMail(Mail):
    def __init__(self, mailbox, subject_name,  tries_to_stop, sleeping_time):
        self.subject_name = subject_name
        self.sleeping_time = sleeping_time
        self.session = GuerrillaMailSession(email_address=mailbox)
        self.content = None
        self.tries_count = tries_to_stop

    def get_code_by_many_tries(self):
        content = None
        for _ in range(self.tries_count):
            for mail in self.session.get_email_list():
                if 'guerrilla' not in mail.sender:
                    content = self.session.get_email(mail.guid).body
                if content:
                    return re.search(r'\b\d{6}\b', content).group()
                else:
                    sleep(self.sleeping_time)
        else:
            return None

