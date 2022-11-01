#!/usr/bin/env python

import re, os, datetime, time, smtplib, ssl

path_dir = os.path.dirname(os.path.realpath(__file__))
filename = os.path.splitext(os.path.basename(__file__))[0]
path_filename = path_dir+os.sep+filename

PROVIDERS = {
    # "AT&T": {"sms": "txt.att.net", "mms": "mms.att.net", "mms_support": True},
    # "Boost Mobile": {"sms": "sms.myboostmobile.com","mms": "myboostmobile.com","mms_support": True,},
    # "C-Spire": {"sms": "cspire1.com", "mms_support": False},
    # "Cricket Wireless": {"sms": "sms.cricketwireless.net ","mms": "mms.cricketwireless.net","mms_support": True,},
    # "Consumer Cellular": {"sms": "mailmymobile.net", "mms_support": False},
    # "Google Project Fi": {"sms": "msg.fi.google.com", "mms_support": True},
    # "Metro PCS": {"sms": "mymetropcs.com", "mms_support": True},
    # "Mint Mobile": {"sms": "mailmymobile.net", "mms_support": False},
    # "Page Plus": {"sms": "vtext.com","mms": "mypixmessages.com","mms_support": True,},
    # "Republic Wireless": {"sms": "text.republicwireless.com","mms_support": False,},
    # "Sprint": {"sms": "messaging.sprintpcs.com","mms": "pm.sprint.com","mms_support": True,},
    # "Straight Talk": {"sms": "vtext.com","mms": "mypixmessages.com","mms_support": True,},
    # "T-Mobile": {"sms": "tmomail.net", "mms_support": True},
    # "Ting": {"sms": "message.ting.com", "mms_support": False},
    # "Tracfone": {"sms": "", "mms": "mmst5.tracfone.com", "mms_support": True},
    # "U.S. Cellular": {"sms": "email.uscc.net","mms": "mms.uscc.net","mms_support": True,},
    # "Verizon": {"sms": "vtext.com", "mms": "vzwpix.com", "mms_support": True},
    # "Virgin Mobile": {"sms": "vmobl.com","mms": "vmpix.com","mms_support": True,},
    # "Xfinity Mobile": {"sms": "vtext.com","mms": "mypixmessages.com","mms_support": True,},
    "Bell":{"sms":"txt.bell.ca","mms":"mms.bell.ca"},
    "Solo Mobile":{"sms":"txt.bell.ca","mms":"mms.bell.ca"},
    "Chatr":{"sms": "pcs.rogers.com",},
    "Rogers":{"sms": "pcs.rogers.com"},
    "Tbaytel":{"sms": "pcs.rogers.com"},
    "Eastlink":{"sms": "txt.eastlink.ca"},
    "Fido":{"sms": "fido.ca"},
    "Koodo Mobile":{"sms": "msg.koodomobile.com"},
    "MTS":{"sms": "text.mtsmobility.com"},
    "PC Mobile":{"sms": "mobiletxt.ca"},
    "Public Mobile":{"sms": "msg.telus.com"},
    "Sasktel":{"sms": "sms.sasktel.com"},
    "TELUS":{"sms": "msg.telus.com"},
    "Virgin":{"sms": "vmobile.ca"},
    "WIND Mobile":{"sms": "txt.windmobile.ca"},
}

def func_gmail(sender:str='reza.s.tahirkheli@gmail.com', password:str='fotbkdhvoasemwwi', email:str='', body:str=''):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, email, body)
    print('\033[32m[+]\033[0m Email Sent: '+email) 

def func_textMsg(sender:str='reza.s.tahirkheli@gmail.com', password:str='fotbkdhvoasemwwi', phone:str='', body:str=''):
    for key in PROVIDERS.keys():
        receiver = f"{phone}@{PROVIDERS.get(key).get('sms')}"

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as email:
            email.login(sender, password)
            email.sendmail(sender, receiver, body)
            
        print('\033[32m[+]\033[0m Phone Text Sent: '+receiver)
        time.sleep(10)

def main():
    try:
        with open(path_filename+'.lst','r') as fout:
            list_entry:str = fout.readlines()
            print(f'\033[32m[+]\033[0m Success: Opening {filename}.lst')
    except:
        print(f'\033[31m[-]\033[0m Could not open {filename}.lst at:\n{path_filename}.lst')

    try:
        with open(path_filename+'.msg','r') as fout:
            str_msg:str  = fout.read()
            print(f'\033[32m[+]\033[0m Success: Opening {filename}.msg')
    except: 
        print(f'\033[31m[-]\033[0m Could not open {filename}.msg at:\n{path_filename}.msg')

    for entry in list_entry:
        try:
            send:bool = True if entry[:4].lower().find('yes') > -1 else False
            email:str = re.search('\s(.+?@.+?\.\w+)',entry).groups()[0]
            phone:str = re.search('(\+\d)?\d{10}',entry).group()
            timestamp = datetime.datetime.today()
            body=f"Subject: {filename}\r\n\r\n{str_msg}"

            if send:

                try:
                    func_gmail(email=email, body=body)
                    with open(path_filename+'.log','a') as fin:
                        fin.write(f'{timestamp} Sent: {email}\n')
                except: pass

                try:
                    func_textMsg(phone=phone, body=body)
                    with open(path_filename+'.log','a') as fin:
                        fin.write(f'{timestamp} Sent: {phone}\n')
                except: print('Failed')
        
        except: pass

if __name__ == '__main__':
    main()
