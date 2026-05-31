#!/usr/bin/env python
# -*- coding: utf-8 -*-

WEB_ROOT_DIR = "../static"

# all the different message types
MSG_SYSTEM_READY = "systemready"
MSG_SYSTEM_SHUTDOWN = "systemshutdown"
MSG_SOCKET_CONNECT = "wsconnect"
MSG_SOCKET_CLOSE = "wsclose"
MSG_SOCKET_MSG = "wsmsg"  # outgoing message to the Browser
MSG_SOCKET_BROWSER = "wsmsgbrowser"  # incoming message from Browser
MSG_DEBUG_QUERY = "debugquery"  # incoming message from Browser
MSG_INPUT_STRING = "inputstring"  # text written on the remote keyboard
MSG_INPUT_SPECIAL = "inputspecial"  # special key pressed on the remote keyboard, e.g. "enter", "backspace", "up", "down", ...
MSG_TVCONTROL_PLAY_STATION = "tvcontrol_play_station"  # message to start playing a station on the TV, data should contain the station URL
MSG_TVCONTROL_SWITCH_VIDEOTEXT_PAGE = "tvcontrol_switch_videotext_page"  # message to switch to a specific videotext page, data should contain the page number
MSG_TVCONTROL_GET_LIST = "tvcontrol_get_list"  # message to get the list of available stations and playlists, data can contain the room name to get the playlist for a specific room, if no room is given, the list of available rooms will be returned
MSG_TVCONTROL_POWER_OFF = "tvcontrol_power_off"  # message to turn off the TV
MSG_TVCONTROL_POWER_ON = "tvcontrol_power_on"  # message to turn on
MSG_TVCONTROL_POWER_SWITCH = "tvcontrol_power_switch"  # message to switch the power state of the TV, if it's on, it will be turned off, if it's off, it will be turned on
MSG_SOCKET_xxx = "xxxx"

# all the different query types
QUERY_PLAYLIST = "satipplaylist"
QUERY_ROOM_NAME = "roomname"

# limits the number of search results when do a query
MAX_QUERY_SIZE = 40
