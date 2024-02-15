
# Classboard

HTML TV display of classes and lab stuf

# Setup

Everything in this project needs to be placed elsewhere on webserver. This is accomplished in production through HARD links as follows, but in general, things need to go in `/var/www/cgi` or `/var/www/html` on cgimisc server:

```
ln /var/www/cgi/evtbrite_TEST.cgi classboard.cgi
ln /var/www/html/classboard.js  classboard.js
ln /var/www/html/classboard.css  classboard.css
ln /var/www/html/EventbriteGeneric.png images/EventbriteGeneric.png
ln /var/www/html/ClassesQR.svg images/ClassesQR.svg
```
