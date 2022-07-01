#!/usr/bin/env python3
'''
based on dhcp-beacon
https://github.com/colonket/dhcp-beacon
Import smtplib for the actual sending function
This script is located on github.com at
https://github.com/rikosintie/dhcp-email.md
'''

__author__ = "Michael Hubbard"
__author_email__ = "michael.hubbard999@gmail.com"
__copyright__ = ""
__license__ = "Unlicense"

import smtplib
# Import the email modules we'll need
from email.message import EmailMessage
from datetime import datetime
from netifaces import interfaces, ifaddresses, AF_INET
from socket import gethostname

from creds import str_username, str_password, list_recipients


def main():
    # Subject
    now = datetime.now().date()
    str_subject = '['+str(now)+'] '+gethostname()+' booted up!'

    # Message
    str_content = ""
    str_content += str('Host: '+gethostname()+'\nTime: '+str(datetime.now())+'\n\n')
    for ifaceName in interfaces():
        # Build list matching interface name to ip addresses
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'N/A'}] )]
        str_content += str(ifaceName+' - '+', '.join(addresses)+'\n')
    print(str_content)

    # Sending Email
    sendEmail(list_recipients, str_subject, str_content)


def sendEmail(list_recipients, str_subject, str_content):
    msg = EmailMessage()
    msg['Subject'] = str_subject
    msg.set_content(str_content)

    # Logistics
    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
    except Exception as e:
        print(str(e))
        exit()
    server.login(str_username, str_password)
    server.sendmail(str_username, list_recipients, str(msg))
    server.quit()
    

if __name__ == "__main__":
    main()
