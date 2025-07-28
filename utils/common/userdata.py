from utils.reg_values_generators import generators
from utils.common.mailbox_interface import EmailBox
from utils.recovery_email import EmailData
import settings


class UserData(EmailBox):
    def __init__(self):
        super().__init__()
        self.__recovery_email: EmailData = None
        self.last_email: EmailData = None
        self.__nickname = None
        self.__password = None
        self.__user_agent = None
        self.__timezone = None

    def generate_new_user(self):
        self.__nickname, self.__password = generators.return_user_data()
        settings.logger.info(f"New user generated!\n"
                             f"Nickname: {self.nickname}\n"
                             f"Password: {self.__password}")

    @property
    def user_agent(self):
        return self.__user_agent

    @property
    def timezone(self):
        return self.__timezone

    def generate_user_agent(self):
        user_agent = generators.generate_user_agent()
        self.__user_agent = user_agent
        settings.logger.info(f"User-agent: {user_agent}")

    def generate_timezone(self):
        timezone = generators.get_timezone()
        self.__timezone = timezone
        settings.logger.info(f"Timezone: {timezone}")

    @property
    def viewport(self):
        return generators.get_viewport()

    @property
    def nickname(self):
        return self.__nickname

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    @property
    def full_email_name_for_verification(self):
        return self.nickname + self.email_domain

    @property
    def verification_code(self):
        return self.get_verification_code(self.nickname)

    @property
    def proton_email_and_proton_password(self):
        return self.nickname + settings.protonmail_domain, self.password

    def get_another_domain(self):
        super().get_another_domain()
        settings.logger.info(f"New domain is {self.email_domain}")

    @property
    def recovery_email(self):
        return self.__recovery_email

    @recovery_email.setter
    def recovery_email(self, rec_email: EmailData):
        self.__recovery_email = rec_email
