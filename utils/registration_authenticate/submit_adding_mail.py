from utils.registration_authenticate.funcs import submit_stuff
from utils.registration_authenticate.funcs.submit_stuff import my_string, submit_adding_email as sbm


def submit_adding_mail(login, password):
    original_string = my_string
    submit_stuff.my_string = my_string.replace("<LOGIN>", login).replace("<PASSWORD>", password)
    res = sbm()
    submit_stuff.my_string = original_string
    return res
