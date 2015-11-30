#!/usr/bin/env python
'''
DESCRIPTION

    Use at to schedule jobs

FOR HELP

    python schedule_jobs.py --help

AUTHOR:      Jake Yeung (jake.yeung@epfl.ch)
LAB:         Computational Systems Biology Lab (http://naef-lab.epfl.ch)
CREATED ON:  2015-11-30
LAST CHANGE: see git log
LICENSE:     MIT License (see: http://opensource.org/licenses/MIT)
'''

import sys, argparse
import csv
import os
from make_send_auto_email import \
    ScheduleRow, \
    parse_date

def get_date_at_format(year, month, day):
    '''
    Get date suitable for at
    man at for possible dates
    '''
    return('.'.join([str(day), str(month), str(year)]))

def make_two_digits(digit):
    '''
    Make 2 digits
    '''
    digit = str(digit)
    if len(digit) == 1:
        return(''.join(["0", digit]))
    else:
        return(digit)

def main():
    parser = argparse.ArgumentParser(description='Use at to schedule jobs')
    parser.add_argument('infile', metavar='INFILE',
                        help='schedule')
    parser.add_argument('run_script', metavar='shellscript',
                        help='shellscript to be run')
    parser.add_argument('--days', '-d', type=int, default = 1,
                        help='Make job launch at d days before event')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress some print statements')
    args = parser.parse_args()

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

    with open(args.infile, 'rb') as inf:
        jreader = csv.reader(inf, delimiter = '\t')
        header = jreader.next()
        for row in jreader:
            Event = ScheduleRow(header, row)
            year, month, day = parse_date(Event.date)
            # send email 1 day before meeting
            day = day - args.days
            month = make_two_digits(month)
            day = make_two_digits(day)
            jdate = ''.join([str(year), str(month), str(day)])
            jtime = "0930"
            date_str = ''.join([jdate, jtime])
            jcommand = "at -m -f %s -t %s" % (args.run_script, date_str)
            # print(jcommand)
            os.system(jcommand)


if __name__ == '__main__':
    main()
