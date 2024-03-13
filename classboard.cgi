#!/usr/bin/python3

import requests
import json
import datetime
import os
import cals
import html
from vars import *

if __name__ == "__main__":
    url = os.environ.get('REQUEST_URI','').split("/")[-1]
    ASSETS = ".."
    VIDEO = "http://127.0.0.1"
    if url == "test.cgi": 
        ASSETS = "../misc"
        VIDEO = "../misc"
    calname=None
    try:
        if ('QUERY_STRING' in os.environ):
            (k,v) = os.environ['QUERY_STRING'].split("=")
            if (k=="cal"):
                calname = v
    except:
        calname=None

    if calname is None or calname=="laser":
        keywords=["MOPA","Epilog","Laser"]
    if calname == "shopbot":
        keywords=["Shopbot"]

    out = {}
    print ("Access-Control-Allow-Origin: *")
    print ("Content-Type: text/html\n\n")

    print (f"""

    <html>
    <head>
    <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
    <script src="{ASSETS}/classboard.js"></script>
    <link rel="stylesheet" href="{ASSETS}/classboard.css">
</head>
""")

    cls={}
    try:
        r = requests.get(f"https://www.eventbriteapi.com/v3/organizations/{ORG_ID}/events/?status=live&expand=ticket_availability&token={TOKEN}")
        
        if ((r.status_code >= 200) and (r.status_code <= 299)):
            j = r.json()

            #print (json.dumps(j,indent=2))

            for x in j['events']:
                n = x['name']['text']
                found = False
                t =  (x['start']['local'])
                # 2023-03-19T10:00:00
                d = datetime.datetime.strptime(t,"%Y-%m-%dT%H:%M:%S")
                ds = d.strftime("%A, %B %d, %I:%M %p")
                l =  x['listed']
                s =  x['ticket_availability']['is_sold_out']
                #print (n,t,l,s,d,ds)
                if l:
                    if n not in out:
                        out[n]=[]
                    out[n].append({"when":ds,"sold_out":s,"sold_out_text":"<b>Sold Out!</b>" if s else ""})
                #print (json.dumps(x,indent=2))

                format_string = "%Y-%m-%dT%H:%M:%S"
                if x['status'] == "live" and x['listed']:
                    starts=datetime.datetime.strptime(x['start']['local'],format_string)
                    if n not in cls:
                        cls[n]={}
                        cls[n]['dates']=[]
                        cls[n]['nextdate']=starts

                    format_string = "%Y-%m-%dT%H:%M:%S"
                    cls[n]['dates'].append({
                        'start':starts,
                        'end':datetime.datetime.strptime(x['end']['local'],format_string),
                        })
                    if x['logo'] is not None:
                        cls[n]['logo']=x['logo']['url']
                    else:
                        cls[n]['logo']=f"{ASSETS}/EventbriteGeneric.png"

                    if (starts < cls[n]['nextdate']): cls[n]['nextdate'] = starts

        print ("<body onload='loadinit()'>")
    except BaseException as e:
        # IF eventbrite load failed - try again in 5 minutes
        print ("<body onload='loadinit()'>")
        print ("<!-- EVENTBRITE ERROR ")
        print (html.escape(str(e)))
        print (" -->")


    print (f"""
<video id="myvideo" width=70% height=70% style="z-index:0;position:absolute;top:20px;right:20px" autoplay loop preload playsinline muted>
  <source class="active" xx-src="file://classvideo.mp4" src="{VIDEO}/classvideo.mp4" />
  Your browser does not support the video tag.
</video>
""")
    print ("<div class='scroll-parent'>")
    print ("<div class='boxes-container'>")

    for x in cls:
        print ("<div class='rounded-box'>")
        print ("<h2>",x,"</h2>")
        num = len(cls[x]['dates'])
        if (num == 1):
            print (f"<p>{cls[x]['nextdate'].strftime('%A %B %-d, %-I:%M %p')}</p>")
        else:
            print (f"<p>{num} dates available<br />\nNext Class:{cls[x]['nextdate'].strftime('%A %B %-d, %-I:%M %p')}</p>")
        print (f"<img src=\"{cls[x]['logo']}\">")
        #for d in sorted(cls[x]['dates'],key=lambda x: x['start']):
        #    print ("   ",d)
        print ("</div>")

    print ("</div> <!-- boxes-container --> ")

    #<!-- We do it twice - to get continuous loop scrolling -->
    print ("<div class='boxes-container2'>")

    for x in cls:
        print ("<div class='rounded-box'>")
        print ("<h2>",x,"</h2>")
        num = len(cls[x]['dates'])
        if (num == 1):
            print (f"<p>{cls[x]['nextdate'].strftime('%A %B %-d, %-I:%M %p')}</p>")
        else:
            print (f"<p>{num} dates available<br />\nNext Class:{cls[x]['nextdate'].strftime('%A %B %-d, %-I:%M %p')}</p>")
        print (f"<img src=\"{cls[x]['logo']}\">")
        #for d in sorted(cls[x]['dates'],key=lambda x: x['start']):
        #    print ("   ",d)
        print ("</div>")

    print ("</div> <!-- boxes-container2 --> ")

    print ("</div> <!-- scroll-parent --> ")

    print ("<div class='qr-rounded-box'>")
    print ("<h4>Classes</h4>")
    print (f"<img src=\"{ASSETS}/ClassesQR.svg\" style=\"width:15vw\">")
    print ("</div class='qr-rounded-box'>")

    # Calendar Boxs
    print ("<div id='calendar' class='cal-container'>")
    print ("<h4>Loading Upcomming Reservations...</h4>")

    """
    for (i,x) in enumerate(cals.upcomming_events()):
        room = x['ROOM']
        organizer = x['ORGANIZER']
        when = x['WHEN']
        summary = x['SUMMARY']
        if '@' in organizer:
            organizer=''
        when = html.escape(when).replace('{}','')[0:30]
        summary = html.escape(summary).replace('{}','')[0:30]
        organizer = html.escape(organizer).replace('{}','')[0:30]
        room = html.escape(room).replace('{}','')[0:30]
        if (i!=0): print ("<hr />")
        print (f"xx""
        <div style="display:flex; justify-content:space-between">
            <div style="align-text:left"><b>{room}</b></div>
            <div style="align-text:right"><b>{when}</b></div>
        </div>
        <div style="display:flex; justify-content:space-between">
            <div style="align-text:left">{summary}</div>
            <div style="align-text:right"><i>{organizer}</i></div>
        </div>
        "xx"")
    """
    print ("</div> <!-- cal-container -->")

    print (f"""
        <div class="centered-container">
            <div id="alert" class="alert hidealert">

                <img height="86px" style="vertical-align:bottom" src="{ASSETS}/MakeItLabsBulb.svg" />
                <tspan id="alert_title" class="alert_title">Welcome!</tspan>
                <hr />
                <tspan id="alert_text" class="alert_text">Firsty McMembername</tspan>
            </div>
        </div>

        <div class="centered-container">
            <div style="display:none" id="alarm" class="alarm">

                <img height="200px" style="vertical-align:bottom" src="{ASSETS}/MakeItLabsBulb.svg" />
                <tspan id="alarm_text" class="alarm_text">Alarm is On!</tspan>
            </div>
        </div>


    """)

    print ("</body>")
    print ("</html>")




