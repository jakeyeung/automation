#!/bin/sh
# Jake Yeung
# clipboard_mails_to_list.sh
# Copy emails from an email body and then convert that to a list 
# 2015-11-30

inf=$1
outf=$2

cat $inf | tr , "\n" |  grep -o '<.*>' | tr -d "<" | tr -d ">" > $outf
