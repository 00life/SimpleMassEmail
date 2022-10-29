#!/usr/bin/env python3
import os, re, datetime, smtplib, ssl

path_dir = os.path.dirname(os.path.realpath(__file__))
filename = os.path.splitext(os.path.basename(__file__))[0]
path_filename = path_dir+os.sep+filename

# Initialize variables
list_entry, str_msg, send, email, timestamp = [], '', False, '', ''

def func_gmail(sender='your@Email.com', password='yourPassword', receiver='', body=''):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, body)
    print('\033[32m[+]\033[0m Email Sent: '+receiver) 

def main():
    try:
        with open(path_filename+'.lst','r') as fout:
            list_entry  = fout.readlines()
            print(f'\033[32m[+]\033[0m Success: Opening {filename}.lst')
    except:
        print(f'\033[31m[-]\033[0m Could not open {filename}.lst at:\n{path_filename}.lst')

    try:
        with open(path_filename+'.msg','r') as fout:
            str_msg  = fout.read()
            print(f'\033[32m[+]\033[0m Success: Opening {filename}.msg')
    except: 
        print(f'\033[31m[-]\033[0m Could not open {filename}.msg at:\n{path_filename}.msg')

    for entry in list_entry:
        try:
            send = True if entry[:4].lower().find('yes') > -1 else False
            email = re.search('\s(.+?@.+?\.\w+)',entry).groups()[0]
            timestamp = datetime.datetime.today()
            body=f"""Subject: {filename}
            \r\n\r\n{str_msg}
            """
            if send: 
                func_gmail(receiver=email, body=body)
                with open(path_filename+'.log','a') as fin:
                    fin.write(f'{timestamp} Sent: {email}\n')
        except: pass

if __name__ == '__main__':
    main()
