import os
import settings
from worker.app_class import App
from utils.common import file_operations
import time

def create_csv_file():
    if not os.path.exists(settings.filename):
        file_operations.create_new_file(
            ('protonmail address',
             'protonmail password',
             'date and time',
             'IP address registered by'))


def main():
    settings.logger.info("Program started")
    accounts_count = input("Enter the number of accounts you want to create (min - 2): ")

    try:
        accounts_count = int(accounts_count)
        if accounts_count < 2:
            raise ValueError('The number of accounts must be at least 2.')
    except ValueError:
        settings.logger.error("Invalid input. Please enter a valid number.")
        return

    create_csv_file()
    app = App()
    for account in app.create_multiple_accounts(accounts_count):
        file_operations.add_to_file(account)
        settings.logger.info(f"Account {account[0]} has been added to file {settings.filename}")
        time.sleep(settings.sleep_between_registrations)

    settings.logger.info("Program stopped")
    input("Press any key to exit...")

if __name__ == '__main__':
    main()
