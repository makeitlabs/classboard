export URL=https://auth.makeitlabs.com/cgi/evtbrite_TEST.cgi
export DISPLAY=:0
unclutter &
chromium-browser $URL --allow-file-access-from-files --force-media-resolution-width 800 --force-media-resolution-height 450 --window-size=800,450 --start-fullscreen --kiosk --incognito --noerrdialogs --disable-translate --no-first-run --fast --fast-start --disable-infobars --disable-features=TranslateUI --disk-cache-dir=/dev/null  --password-store=basic --enable-logging=stderr
#MOS_ENABLE_WAYLAND=1 firefox --kiosk $URL
