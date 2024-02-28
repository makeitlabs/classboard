#!/usr/bin/python3

import requests
import json
import datetime
import os
from vars import *

if __name__ == "__main__":
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

    print ("""

    <html>
    <head>
    <script src="../misc/classboard.js"></script>
    <link rel="stylesheet" href="../misc/classboard.css">
</head>
""")

    r = requests.get(f"https://www.eventbriteapi.com/v3/organizations/{ORG_ID}/events/?status=live&expand=ticket_availability&token={TOKEN}")
    
    cls={}
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
                    cls[n]['logo']="../misc/EventbriteGeneric.png"

                if (starts < cls[n]['nextdate']): cls[n]['nextdate'] = starts

    print ("<body onload='loadinit()'>")


    print ("""
<video id="myvideo" width=60% height=60% style="z-index:0;position:absolute;top:20px;right:20px" autoplay loop preload playsinline muted>
  <source class="active" src="../misc/classvideo.mp4" />
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
    print (f"<img src=\"../misc/ClassesQR.svg\" style=\"width:15vw\">")
    print ("</div class='qr-rounded-box'>")

    # Calendar Boxs
    print ("<div class='cal-container'>")
    print ("This is a test")
    print ("</div> <!-- cal-container -->")

    print ("</body>")
    print ("</html>")




