#!/usr/bin/env python
'''
DESCRIPTION

    Write email reminders of circadian meeting

FOR HELP

    python circadian_meeting_reminder.py --help

AUTHOR:      Jake Yeung (jake.yeung@epfl.ch)
LAB:         Computational Systems Biology Lab (http://naef-lab.epfl.ch)
CREATED ON:  2015-11-30
LAST CHANGE: see git log
LICENSE:     MIT License (see: http://opensource.org/licenses/MIT)
'''

import sys, argparse
import csv
import os
from datetime import date

class ScheduleRow():
    def __init__(self, header, row):
        '''
        First column must be date, others will be
        specificied based on header (first row)
        then we replace header with event info in msg body
        '''
        self.date = row[0]
        self.header = header
        self.params = {}
        for h in header:
            self.params[h] = row[header.index(h)]

def parse_date(datestr, delim = '-'):
    '''
    2015-11-30 -> 2015, 11, 30
    '''
    year = int(datestr.split(delim)[0])
    month = int(datestr.split(delim)[1])
    day = int(datestr.split(delim)[2])
    return(year, month, day)

def get_date_obj_from_str(datestr):
    '''
    2015-11-30 -> date obj expect
    '''
    year, month, day = parse_date(datestr)
    return(date(year, month, day))

def delta_days(date_later, now):
    '''
    Return days between two dates. Later - Earlier
    '''
    later = get_date_obj_from_str(date_later)
    delta = later - now
    return delta.days

def get_nearest_event(inf, delta_max=3):
    '''
    Tabsep file with date, location, speaker, title of talk
    return row that is upcoming

    delta_max: complain if too many days before talk
    '''
    with open(inf, 'rb') as readfile:
        jreader = csv.reader(readfile, delimiter = '\t')
        header = jreader.next()
        for row in jreader:
            Row = ScheduleRow(header, row)
            day_delta = delta_days(Row.date, date.today())
            if day_delta > delta_max:
                sys.exit("Too many days before next talk")
            else:
                return(Row)

def generate_message(msg_path, Event):
    '''
    Generate message replacing <+DATE+> <+LOCATION+> <+SPEAKER+> <+TITLE+>
    with Event info
    '''
    message_obj = open(msg_path, "rb")
    message = message_obj.read()
    for h in Event.header:
        message = message.replace(h, Event.params[h])
    return(message)

def get_emails(emails_path, outsep = ","):
    '''
    Get list of emails into a separated format
    '''
    emails_obj = open(emails_path, "rb")
    emails = emails_obj.read()
    emails = emails.replace("\n", outsep)
    # if last character is ",", remove it
    if emails.endswith(outsep):
        emails = emails[:-1]
    return emails

def generate_mail_script_path(emails, subject, msg_path):
    '''
    echo "Hello" | mail -s "Test" jake.yeung@epfl.ch,jingkui.wang@epfl.ch

    Output something that can be parsed through os.system()
    '''
    bash_script = ''.join(['cat ', msg_path, ' | mail -s "', subject, '" ', emails])
    return(bash_script)

def generate_mail_script(emails, subject, msg):
    '''
    echo "Hello" | mail -s "Test" jake.yeung@epfl.ch,jingkui.wang@epfl.ch

    Output something that can be parsed through os.system()
    '''
    bash_script = ''.join(['echo "', msg, '" | mail -s "', subject, '" ', emails])
    return(bash_script)

def get_subject(sub_path):
    sub_obj = open(sub_path, "rb")
    sub = sub_obj.read().rstrip()
    return(sub)

def save_to_temp(msg, temp):
    temp_obj = open(temp, "wb")
    temp_obj.write(msg)

def main():
    parser = argparse.ArgumentParser(description='Write email reminders')
    parser.add_argument('--schedule', required=True, metavar='INFILE',
                        help='Tabsep file with date, location, speaker, title talk')
    parser.add_argument('--emails', required=True, metavar='INFILE2',
                        help='List of emails')
    parser.add_argument('--message_body', required=True, metavar='INFILE3',
                        help='Body of message with <+ +> tags to be replaced with schedule info')
    parser.add_argument('--subject', required=True, metavar='INFILE4',
                        help='Email subject as a textfile')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress some print statements')
    parser.add_argument('--preview', '-p', action='store_true',
                        help='Preview message but dont send it')
    args = parser.parse_args()

    MSG_TMP_FILE="/tmp/email_body.txt"

    # store command line arguments for reproducibility
    CMD_INPUTS = ' '.join(['python'] + sys.argv)    # easy printing later
    # store argparse inputs for reproducibility / debugging purposes
    args_dic = vars(args)
    ARG_INPUTS = ['%s=%s' % (key, val) for key, val in args_dic.iteritems()]
    ARG_INPUTS = ' '.join(ARG_INPUTS)

    # Print arguments supplied by user
    if not args.quiet:
        print('Command line inputs:')
        print(CMD_INPUTS)
        print ('Argparse variables:')
        print(ARG_INPUTS)

    Event = get_nearest_event(args.schedule)
    msg = generate_message(args.message_body, Event)
    save_to_temp(msg, MSG_TMP_FILE)
    emails = get_emails(args.emails, outsep = ",")
    subject = get_subject(args.subject)
    sendscript = generate_mail_script_path(emails, subject, MSG_TMP_FILE)
    # sendscript = generate_mail_script(emails, subject, msg)
    if args.preview:
        print("Sending to: %s" %emails)
        print("Subject: %s" %subject)
        print("Msg: %s" %msg)
        print("Script: ")
        print(sendscript)
        print("In preview mode: DID NOT SEND")
    else:
        print("Sending to: %s" %emails)
        print("Subject: %s" %subject)
        print("Msg: %s" %msg)
        os.system(sendscript)
        print("Ran script: %s" %sendscript)

if __name__ == '__main__':
    main()
