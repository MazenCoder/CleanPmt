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

class Loadfile:

    def init_load(self):
        # check all path
        pathes = ['outcsv'+os.sep+'delivered', 'outcsv'+os.sep+'bounce', 'outcsv'+os.sep+'quota', 'outcsv'+os.sep+'clean', 'archives']
        for path in pathes:
            if not os.path.exists(path):
                return
            else:
                fields = os.listdir(path)
                print('fields: ', fields)
                for file in fields:
                    if file != '.DS_Store':
                        if os.path.isfile(path+os.sep+file):
                            os.remove(path+os.sep+file)
                        else:
                            shutil.rmtree(path+os.sep+file)

        # clean cvs
        arr = os.listdir("incsv")
        print('arr: ', arr)
        for t_file in arr:
            if t_file != '.DS_Store':
                self.clean_email(t_file)
                shutil.move("incsv"+ os.sep + t_file, 'archives')

        stock_file = sorted(glob("outcsv"+os.sep+"*.csv"))
        print(stock_file)

    def clean_email(self, fichier):
        try:
            list_delivered = []
            list_bounce = []
            list_quota = []
            list_clean = []

            rg_1 = '2.0.0 (success)'
            rg_2 = "(user|mailbox|recipient|rcpt|local part|address|account|mail drop|ad(d?)ressee) (has|has been|is)? *(currently|temporarily+)?(disabled|expired|inactive|not activated)|(user|mailbox|recipient|rcpt|local part|address|account|mail drop|ad(d?)ressee) +(\S+@\S+ +)?(not (a +)?valid|not known|not here|not found|does not exist|bad|invalid|unknown|illegal|unavailable)|(No such|bad|invalid|unknown|illegal|unavailable) (local +)?(user|mailbox|recipient|rcpt|local part|address|account|mail drop|ad(d?)ressee)|have a \S+ account|Recipient address rejected|ccount has been disabled or discontinued|no valid recipie|Account Inactive|inactive-mailbox|[45]\.1\.[1346]|[45]\.1\.2|[45]\.2\.0;|[45]\.2\.1|[45]\.1\.1|user doesn't|User Unknown|user Unknown|Bad email address|Mailbox full|no email address|no such|not found|user doesn't|exist|Not a valid recipient|address rejected|such as not found|Userís mailbox was unavailable|Bad destination|This mailbox is disabled|No Such User Here|hardbnc|(conta|usu.rio) inativ(a|o)|\S+@\S+ +(is +)?(not (a +)?valid|not known|not here|not found|does not exist|bad|invalid|unknown|illegal|unavailable)|no mailbox here by that name|my badrcptto list|not our customer|no longer (valid|available)|domain (retired|bad|invalid|unknown|illegal|unavailable)|domain no longer in use|domain no longer in use|domain (\S+ +)?(is +)?obsolete"
            rg_3 = "5\.1\.1|5\.1\.2|5\.1\.3|5\.1\.4|5\.1\.5|5\.1\.6|5\.1\.7|5\.2\.1|5\.2\.2|5\.2\.3|5\.2\.4|4\.2\.2|5\.3\.1"

            with open('incsv'+ os.sep + fichier, 'r') as scv_file:
                csv_dict_reader = csv.DictReader(scv_file)
                for row in csv_dict_reader:
                    data_row = row['dsnStatus'] + ' ' + row['dsnDiag'] + ' ' + row['bounceCat']
                    print('data_row:', data_row)
                    # re1_result = re.match(rg_2, data_row)
                    re1_result = re.search(rg_2, data_row)
                    re2_result = re.search(rg_3, data_row)

                    if row['dsnStatus'] == rg_1:
                        list_delivered.append(row['rcpt'])
                    elif re1_result:
                        print('bounce --> ', row['rcpt'])
                        list_bounce.append(row['rcpt'])
                    elif re2_result:
                        print('quota -> ', row['rcpt'])
                        list_quota.append(row['rcpt'])
                    else:
                        print('clean -> ', row['rcpt'])
                        list_clean.append(row['rcpt'])

            scv_file.close()

            # names of csv files
            filedelivered = 'outcsv'+os.sep+'delivered'+os.sep+'delivered_' + fichier
            filedbounce = 'outcsv'+os.sep+'bounce'+os.sep+'bounce_' + fichier
            fileqouta = 'outcsv'+os.sep+'quota'+os.sep+'quota_' + fichier
            fileclean = 'outcsv'+os.sep+'clean'+os.sep+'clean_' + fichier

            # writing bounce email to csv file
            with open(filedelivered, 'w', newline='') as deliveredfile:
                order = csv.writer(deliveredfile)
                # order.writerow(['email'])
                for email in list_delivered:
                    if email != 'rcpt':
                        order.writerow([email])
            deliveredfile.close()

            # writing bounce email to csv file
            with open(filedbounce, 'w', newline='') as bouncefile:
                order = csv.writer(bouncefile)
                # order.writerow(['email'])
                for email in list_bounce:
                    if email != 'rcpt':
                        order.writerow([email])
            bouncefile.close()

            # writing quota email to csv file
            with open(fileqouta, 'w', newline='') as qoutafile:
                order = csv.writer(qoutafile)
                # order.writerow(['email'])
                for email in list_quota:
                    order.writerow([email])
            qoutafile.close()

            # writing clean email to csv file
            with open(fileclean, 'w', newline='') as cleanfile:
                order = csv.writer(cleanfile)
                # order.writerow(['email'])
                for email in list_clean:
                    if email != 'rcpt':
                        order.writerow([email])
            cleanfile.close()

        except Exception as e:
            print(e)

    def merge_csv(self):
        pathes = ['outcsv'+os.sep+'delivered', 'outcsv'+os.sep+'bounce', 'outcsv'+os.sep+'quota', 'outcsv'+os.sep+'clean']
        for path in pathes:
            print(path)
            source_files = sorted(Path(path).glob('*.csv'))
            if source_files:
                all_together = ""
                for file in source_files:
                    with open(file, 'r') as f:
                        all_together = f"{all_together}{f.read()}"
                    os.remove(file)

                with open(path+os.sep+'merge.csv', 'w', newline='') as f:
                    f.write(all_together)

                clean_set = []
                with open(path+os.sep+'merge.csv', 'r') as scv_file:
                    csv_dict_reader = csv.reader(scv_file)
                    for row in csv_dict_reader:
                        clean_set.append(row[0].replace(' ', ''))

                clean_list = list(dict.fromkeys(clean_set))
                print('clean_list: ', clean_list)

                # writing finally email to csv file
                with open(path+os.sep+'finally.csv', 'w', newline='') as finallyfile:
                    order = csv.writer(finallyfile)
                    for email in clean_list:
                        order.writerow([email])
                finallyfile.close()
                os.remove(path+os.sep+'merge.csv')

    def div_email(self, path, file):
        print(path, file)
        list_email = []
        list_domain = []
        clear_domain = []

        with open(file, 'r') as scv_types:
            csv_dict_reader = csv.reader(scv_types)
            for row in csv_dict_reader:
                list_domain.append(self.regex_email(row[0].replace(' ', '')))
                list_email.append(row[0].replace(' ', ''))

            clear_domain = list(dict.fromkeys(list_domain))
            self.creat_files(path, list_email, clear_domain)
            os.remove(file)

    def email_splitter(self, email):
        domain = email.split("@")[1]
        name = domain.split(".")[0]
        print(name)
        return name

    def regex_email(self, email):
        regex = re.search(r'(.+)@(.+)\.(.+)', email)
        domain = regex.group(3)
        print(domain)
        return domain.lower()

    def creat_files(self, path, emails, domains):
        email_content_domain = []
        print(domains)
        for domain in domains:
            for email in emails:
                if email.endswith('.' + domain):
                    email_content_domain.append(email)


            os.mkdir(path + domain)
            write_path = path + domain +os.sep+ domain + '_.csv'
            with open(write_path, 'w', newline='') as write:
                order = csv.writer(write)
                for ecd in email_content_domain:
                    order.writerow([ecd])
            write.close()
            email_content_domain.clear()

    def split_file(self):
        # pathes = ['outcsv/delivered', 'outcsv/bounce', 'outcsv/quota', 'outcsv/clean']
        pathes = ['outcsv'+os.sep+'delivered', 'outcsv'+os.sep+'clean']
        for path in pathes:
            if not os.path.exists(path):
                return
            else:
                fields = sorted(glob(path+os.sep+"*.csv"))
                print('fields: ', fields)
                print('fields: ', path+os.sep)
                for file in fields:
                    self.div_email(path+os.sep, file)

    def split_domain(self):
        pathes = ['outcsv'+os.sep+'delivered', 'outcsv'+os.sep+'bounce', 'outcsv'+os.sep+'quota', 'outcsv'+os.sep+'clean']
        for path in pathes:
            if not os.path.exists(path):
                return
            else:
                fields = os.listdir(path)
                for file in fields:
                    self.split_email(path+os.sep+ file)

    def split_email(self, path):
        fields = sorted(glob(path+os.sep+"*.csv"))
        for file in fields:
            if file:
                list_email = []
                list_domain = []
                clear_domain = []

                with open(file, 'r') as scv_types:
                    csv_dict_reader = csv.reader(scv_types)
                    for row in csv_dict_reader:
                        list_domain.append(self.email_splitter(row[0].replace(' ', '')))
                        list_email.append(row[0].replace(' ', ''))

                    clear_domain = list(dict.fromkeys(list_domain))
                    print("clear_domain: ", clear_domain)
                    self.creat_cvs_by_domain(path, list_email, clear_domain)
                    os.remove(file)

    def creat_cvs_by_domain(self, path, list_email, list_domain):
        email_content_domain = []
        for domain in list_domain:
            for email in list_email:
                if self.check_domain(email, domain):
                    email_content_domain.append(email)

            with open(path+os.sep+ domain+'__.csv', 'w', newline='') as cleanfile:
                order = csv.writer(cleanfile)
                for row in email_content_domain:
                    order.writerow([row])
            cleanfile.close()
            email_content_domain.clear()


    def check_domain(self, email, current_domain):
        try:
            domain = email.split("@")[1]
            name = domain.split(".")[0]
            print(name)
            if name == current_domain:
                print('check_domain-1 :', name + ' 2: ' + current_domain)
                return True
            else:
                print('check_domain-1 :', name + ' 2: ' + current_domain)
                return False

        except Exception as e:
            return False


if __name__ == '__main__':
    Loadfile().init_load()
    # finally
    # Loadfile().merge_csv()

    # Loadfile().split_file()
    # Loadfile().split_domain()
