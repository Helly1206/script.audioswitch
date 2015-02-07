#!/bin/bash

LOG_FILE_XBMC=$1 #"/home/helly/.kodi/temp/kodi.log"
AMOUNT=8
DEBUG=0

#find latest audio enumeration in log file
AUDIO_LINE=$(cat $LOG_FILE_XBMC|grep -n "Enumerated ALSA devices"|tail -n 1|awk 'BEGIN { FS = ":" } ; { print $1 }'|bc)

if [ $DEBUG -gt 0 ]; then
    echo "Line to start:" $AUDIO_LINE
fi

if [ $AUDIO_LINE -gt 0 ]; then
    CONT=1
    INDEX=1
    while [ $CONT -gt 0 ]
    do
        START=$(echo $AUDIO_LINE+1|bc)
        CMP_DEVICE=$(echo "Device "$INDEX)
        AUDIO_DEVICE=$(cat $LOG_FILE_XBMC|head -$START|tail -1|awk '{print $4" "$5}')
        if [ "$AUDIO_DEVICE" = "$CMP_DEVICE" ]; then
            #echo $AUDIO_DEVICE
            START=$(echo $AUDIO_LINE+2|bc)
            DEVICENAME=$(cat $LOG_FILE_XBMC|head -$START|tail -1|awk '{ s = ""; for (i = 6; i <= NF; i++) s = s $i " "; print s }')
            #echo $DEVICENAME
            if [ -z "$DEVICENAME" ]; then
                DEVICENAME="Option$INDEX"            
            fi
 	    START=$(echo $AUDIO_LINE+4|bc)
            DISPLAYNAMEEXTRA=$(cat $LOG_FILE_XBMC|head -$START|tail -1|awk '{ s = ""; for (i = 6; i <= NF; i++) s = s $i " "; print s }')
            #echo $DISPLAYNAMEEXTRA
            if [ -z "$DISPLAYNAMEEXTRA" ]; then
                START=$(echo $AUDIO_LINE+3|bc)
                DISPLAYNAME=$(cat $LOG_FILE_XBMC|head -$START|tail -1|awk '{ s = ""; for (i = 6; i <= NF; i++) s = s $i " "; print s }')
            else
                DISPLAYNAME=$(echo $DISPLAYNAMEEXTRA)            
            fi

            #echo output
            echo -e $DEVICENAME"\t"$DISPLAYNAME            

            CONT=1
            AUDIO_LINE=$(echo $AUDIO_LINE+$AMOUNT|bc)
            ((INDEX++))
        else
            CONT=0
        fi
    done
fi


