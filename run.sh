#!/bin/bash
 
while true; do
   
    requestresult=$(python jenkinsrequest.py)
   
    if[$requestresult -ne "none"]
    then
        notifyinfo=($(echo $requestresult | tr ',' "\n"))
        notify-send -i $notifyinfo[1] "${notifyinfo[2]}" "${notifyinfo[3]}"
    fi
 
    sleep 30m
done