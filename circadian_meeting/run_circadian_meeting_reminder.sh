#!/bin/sh
# Jake Yeung
# run_circadian_meeting_reminder.sh
# Run it 
# 2015-11-30

pyscript="/Users/yeung/scripts/automation/make_send_auto_email.py"
sched="/Users/yeung/scripts/automation/circadian_meeting/circadian_meeting.schedule"
email="/Users/yeung/scripts/automation/circadian_meeting/circadian_meeting.emails"
# email="/Users/yeung/scripts/automation/circadian_meeting/circadian_meeting.emails.test"
msg="/Users/yeung/scripts/automation/circadian_meeting/circadian_meeting.message"
sub="/Users/yeung/scripts/automation/circadian_meeting/circadian_meeting.subject"

[[ ! -e $pyscript ]] && echo "$pyscript not found, exiting" && exit 1
[[ ! -e $sched ]] && echo "$sched not found, exiting" && exit 1
[[ ! -e $email ]] && echo "$email not found, exiting" && exit 1
[[ ! -e $msg ]] && echo "$msg not found, exiting" && exit 1
[[ ! -e $sub ]] && echo "$sub not found, exiting" && exit 1

python $pyscript --schedule $sched --emails $email --message $msg --subject $sub

if [[ $? = 0 ]]; then
    echo "success"
	echo "Auto-send success" | mail -s "Auto-send success" jake.yeung@epfl.ch
else
    echo "failure: $?"
	echo "Auto-send failed" | mail -s "Auto-send failed" jake.yeung@epfl.ch
fi
