import time
import vlc

player = vlc.MediaPlayer(
    "satip://megasat/?src=1&freq=11494&pol=h&ro=0.35&msys=dvbs2&mtype=8psk&plts=on&sr=22000&fec=23&pids=0,17,18,5100,5101,5102,5104"
)

if player:
    print("VLC media player instance created successfully.")
    player.play()
    time.sleep(5)
    player.pause()
    time.sleep(10)
    player.play()
    time.sleep(10)

    player.video_set_teletext(411)
    time.sleep(20)
    player.video_set_teletext(0)
    time.sleep(10)

else:
    print("Failed to create VLC media player instance.")
