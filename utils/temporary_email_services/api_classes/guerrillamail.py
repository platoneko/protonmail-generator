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
        import settings as _s
        _s.logger.info(f"Polling guerrillamail for address: {self.session.email_address}")
        for attempt in range(1, self.tries_count + 1):
            _s.logger.info(f"GuerrillaMail poll attempt {attempt}/{self.tries_count}")
            mail_list = self.session.get_email_list()
            _s.logger.info(f"Got {len(mail_list)} emails in inbox")
            for mail in mail_list:
                _s.logger.info(f"  Mail from: {mail.sender} | subject: {mail.subject}")
                if 'guerrilla' not in mail.sender:
                    content = self.session.get_email(mail.guid).body
                    match = re.search(r'\b\d{6}\b', content)
                    if match:
                        return match.group()
            sleep(self.sleeping_time)
        return None

