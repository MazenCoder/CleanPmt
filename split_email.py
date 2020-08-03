from numpy import random
from pathlib import Path
from glob import glob
import pandas as pd
import fileinput
import shutil
import sys
import csv
import os
import re

class SplitEmail:

    def div_email(self):

        list_email = []
        list_domain = []
        clear_domain = []
        files_email = sorted(glob("email/*.csv"))
        for file_csv in files_email:
            with open(file_csv, 'r') as file:
                #csv_dict_reader = csv.DictReader(file)
                csv_dict_reader = csv.reader(file)
                for row in csv_dict_reader:
                    list_domain.append(self.regex_email(row[0].replace(' ', '')))
                    list_email.append(row[0].replace(' ', ''))

                clear_domain = list(dict.fromkeys(list_domain))
        self.creat_files(list_email, clear_domain)

    def regex_email(self, email):
        # regex = re.search(r'([a-zA-Z0-9./-]+)@([a-zA-Z0-9./-]+)\.([a-z]+)', email)
        regex = re.search(r'(.+)@(.+)\.(.+)', email)
        domain = regex.group(3)
        print(domain)
        return domain

    def email_splitter(self, email):
        username = email.split('@')[0]
        domain = email.split('@')[1]
        domain_name = domain.split('.')[0]
        domain_type = ''
        try:
            domain_type = domain.split('.')[2]
        except Exception as e:
            domain_type = domain.split('.')[1]
        # print('Username : ', username)
        # print('Domain   : ', domain_name)
        print('Type     : ', domain_type)
        return domain_type

    def creat_files(self, emails, domains):
        email_content_domain = []
        for domain in domains:
            for email in emails:
                if email.endswith('.'+domain):
                    email_content_domain.append(email)

            with open('email/'+domain+'_.csv', 'w', newline='') as write:
                order = csv.writer(write)
                for ecd in email_content_domain:
                    order.writerow([ecd])
            write.close()
            email_content_domain.clear()






if __name__ == '__main__':
    SplitEmail().div_email()

