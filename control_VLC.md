# Notizssammlung für einen VLC controller

Kurzanleitung für VLC im Raspi- Kiosk-Mode: https://github.com/altugdurmaz/rpi-vlc-kiosk

## Startsequenz für vlc

Der Player will immer ein HTTP password, der Username ist ein leerer String ("")

  vlc --intf http  --http-password tv "rtsp://exip418/?src=1&freq=11494&pol=h&ro=0.35&msys=dvbs2&mtype=8psk&plts=on&sr=22000&fec=23&pids=0,17,18,5100,5101,5102,5104"

  DISPLAY=:0 vlc  --osd --intf http  --http-password tv  "rtsp://exip418/?src=1&freq=11494&pol=h&ro=0.35&msys=dvbs2&mtype=8psk&plts=on&sr=22000&fec=23&pids=0,17,18,5100,5101,5102,5104"


Dann können per URL Kommandos gegeben werden:

  wget --user "" --password tv  'http://127.0.0.1:8080/requests/status.xml?command=in_play&input=rtsp%3A%2F%2Fexip418%2F%3Fsrc%3D1%26freq%3D11494%26pol%3Dh%26ro%3D0.35%26msys%3Ddvbs2%26mtype%3D8psk%26plts%3Don%26sr%3D22000%26fec%3D23%26pids%3D0%2C17%2C18%2C5100%2C5101%2C5102%2C5104'

Der eigentliche URL zum Abspielen ("input=") muß URL-Encoded ! angegeben werden



## Verzweifelte Versuche, das Telnet- Interface ans Laufen zu kriegen...

Mit

cvlc --vbi-opaque true --intf telnet --telnet-host="0.0.0.0:4012" --telnet-password=tv --extraintf http  --http-password tv "rtsp://exip418/?src=1&freq=11494&pol=h&ro=0.35&msys=dvbs2&mtype=8psk&plts=on&sr=22000&fec=23&pids=0,17,18,5100,5101,5102,5104"


war auf port eine lokale Telnet - Verbindung möglich, auch wenn der Port 4012 NICHT von nmap als offener Port gezeigt wird (Danke für nichts..)


Erste Erfolge: mit 'key subtitle-toggle' im Telnet Fenster ging 


Track des Videotextes???

      --sub-track=<integer>      Subtitle track
          Stream number of the subtitle track to use (from 0 to n).

                --global-key-subtitle-toggle=<string> 
                                 Toggle subtitles

hässlicher Fehler beim Teletext- Overlay:


Begründung:
https://forums.raspberrypi.com/viewtopic.php?t=386007#p2306955



x-window server

sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox

Ausführen: https://raspberrypi.stackexchange.com/a/92199

sudo nano /etc/xdg/openbox/autostart

xset s off
xser s noblank
xset -dpms
vlc  --vbi-opaque --no-osd --fullscreen --extraintf http,telnet  --http-passwor>





## experimentelles keystroke senden

https://stackoverflow.com/a/12096748


Und vielleicht die Endlösung??

https://pypi.org/project/python-vlc/

