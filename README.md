# SATIP Playlists
This program provides a real time filter for SATIP m3u playlists from the internet.

Many popular SATIP players, like VLC or Kodi, allows or wants to have downloadable playlists (m3u) to show the available TV stations.

There are great resources in the net (like [dersnyke](https://github.com/dersnyke/satipplaylists)), but these static files have one problem: As they contain all available stations, they are much too long.

To make individual downloadable favorite lists out of them, *SATIP Playlists (SPL)* was made.

To be available 24/7, it's been made as a docker application, so you'll need your own local docker server for it.

SPL acts like a proxy: After initial favorite configuration, you can use the SPLs url for all your players. When then a player downloads his playlist from SPL, SPL catches the full playlist from the internet in the background, filters the favorites and provides the favorite list with its actual urls to the player.

Several favorite lists can be configured, so each player can have its individual list

## Setup
As the SPL container exposes its configuration files into a local directory, you'll need to find such place first on your docker server. If you have, then cd into it and run

   git clone https://github.com/stko/satip_playlists.git
   cd satip_playlists
   docker compose up --build

SPL now creates the inital config directory structures. End the program straight again with CRTL+C. Now as next activate the plugins by editing 

   sudo nano satipPlaylistName-backup/PluginManager/plugins.json 

and set `active`of all plugins to `true`. Restart the container again (`docker compose up`) and stop it again with CRTL+C.

Now you can edit all your favorite settings in 

  sudo nano satipPlaylistName-backup/satipplaylists/config.json

and start SPL finally to run in the background with `docker compose up -d`

Now you can access your personal playlists at `http://<your_docker_server>:8075/<playlist_name>`

# Limitations
Obviously neither this documentation, the installation nor the web gui is state of the art, because this project was made as a works-for-me on a cloudy autumn day. But maybe anybody would like to jump into and brings a little bit more salt and pepper into it?

  