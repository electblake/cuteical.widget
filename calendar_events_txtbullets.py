#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import hashlib
import conf

def prettify_calendar():
    html = ""
    bullets = ["<span class='square'>■</span>", "<span class='heart'>♥</span>",
               "<span class='triangle'>▼</span>", "<span class='circle'>●</span>"]
    bullet_counter = 0
    icalbinary = "/usr/local/bin/icalBuddy"

    exclude_calendar_ids = conf.exclude_calendar_ids

    exclude_event_properties = [
        "location",
        "url",
        "notes",
        "attendees"
    ]

    calendar_names = "-nc" # no calendar names, use "" to include

    # ignore_past_events = "--includeOnlyEventsFromNowOn"
    ignore_past_events = ""

    # remove error from icalbuddy and get calendar info for today
    with open(os.devnull, 'w') as devnull:
        try:
            raw_events = subprocess.check_output([icalbinary, "-nrd", calendar_names, ignore_past_events, "-b", "❤︎ ",
                                                  "--excludeCals", ",".join(exclude_calendar_ids),
                                                  "-eep", ",".join(exclude_event_properties), "eventsToday"], stderr=devnull)
            html, bullet_counter = display_events(
                html, "Today", raw_events, bullets, bullet_counter)
        except subprocess.CalledProcessError as e:
            print("Error with icalBuddy: ", e.message)

    # remove error from icalbuddy and get calendar info for tomorrow
    with open(os.devnull, 'w') as devnull:
        try:
            raw_events = subprocess.check_output([icalbinary, "-nrd", calendar_names, ignore_past_events, "-b", "❤︎ ",
                                                  "--excludeCals", ",".join(exclude_calendar_ids),
                                                  "-eep", ",".join(exclude_event_properties), "eventsFrom:today+1", "to:today+1"], stderr=devnull)
            html, bullet_counter = display_events(
                html, "Tomorrow", raw_events, bullets, bullet_counter)
        except subprocess.CalledProcessError as e:
            print("Error with icalBuddy: ", e.message)

    print(html)

def display_events(html, what_day, raw_events, bullets, bullet_counter):
    events = raw_events.split("\n")
    listed_events = []
    # display events for the day
    if len(events) < 2:
        html += "<div class='today'>\n<div class='title'>No events planned for " + \
            what_day.lower()+"</div>\n</div>"
    else:
        html += "<div class='today'>\n<div class='title'>"+what_day+"'s Events</div>"
        for i in range(len(events)):
            hashid = hashlib.md5(str(events[i])).hexdigest()
            if (hashid not in listed_events):
                listed_events.append(hashid)
                if events[i].find("❤︎") != -1:
                    html += "\n<div class='event_title'>" + \
                        events[i].replace("❤︎", bullets[bullet_counter])+"</div>"
                    if bullet_counter < 3:
                        bullet_counter += 1
                    else:
                        bullet_counter = 0
                elif events[i] == "":
                    pass
                else:
                    html += "\n<div class='event_time'>"+events[i]+"</div>"
        # close  div
        html += "\n</div>"
    return html, bullet_counter


prettify_calendar()
