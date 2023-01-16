#!/bin/bash

read_info() {
  file=$1
  folder=$(dirname $file)
  if [[ -f $file ]]; then
    title=$(/usr/libexec/PlistBuddy $file -c 'Print :Title')
    uuid=$(/usr/libexec/PlistBuddy $file -c 'Print :Key')
    echo "$title,$uuid,$file"
  fi
}

find ~/Library/Calendars -name "Info.plist" | while read file; do
  read_info $file | column -t -s ','
done