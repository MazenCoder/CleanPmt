
class RegexEmail:

    def email_splitter(self, email):
        username = email.split('@')[0]
        domain = email.split('@')[1]
        domain_name = domain.split('.')[0]
        domain_type = ''
        try:
            domain_type = domain.split('.')[2]
        except Exception as e:
            domain_type = domain.split('.')[1]

        print('Username : ', username)
        print('Domain   : ', domain_name)
        print('Type     : ', domain_type)




if __name__ == '__main__':
    # RegexEmail().email_splitter('michael@amrita-naturverbindung.ch')
    RegexEmail().email_splitter('joshuaanthony09@yahoo.com.ph')
    # RegexEmail().email_splitter('maniek87@op.pl')