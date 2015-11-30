#!/bin/sh
# Jake Yeung
# run_circadian_meeting_reminder.sh
# Run it 
# 2015-11-30

pyscript="make_send_auto_email.py"
sched="circadian_meeting.schedule"
email="circadian_meeting.emails.test"
msg="circadian_meeting.message"
sub="circadian_meeting.subject"

python $pyscript --schedule $sched --emails $email --message $msg --subject $sub
