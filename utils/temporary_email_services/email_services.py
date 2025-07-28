from collections import namedtuple
from .api_classes.guerrillamail import GuerrillaMail
# from .api_classes.maildrop import MailDrop

Service = namedtuple('Service', 'name_of_service class_of_service domain_name')

services = [
    Service('guerrillamail', GuerrillaMail, '@guerrillamail.com'),
    # Service('maildrop', MailDrop, '@maildrop.cc'),
]
