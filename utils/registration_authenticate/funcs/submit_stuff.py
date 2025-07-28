my_string = f"""   
from protonmail import ProtonMail
from bs4 import BeautifulSoup

proton = ProtonMail()
proton.login("<LOGIN>", r"<PASSWORD>")

# Get a list of all messages
messages = proton.get_messages()

# Read the latest message
message = proton.read_message(messages[0])

soup = BeautifulSoup(message.body, 'html.parser')
link = soup.find('a')
result = link.get('href')
"""

submit_adding_email = lambda: (lambda ctx={}: (exec(my_string, {}, ctx), ctx.get('result'))[1])()
