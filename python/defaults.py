#!/usr/bin/env python
# -*- coding: utf-8 -*-

WEB_ROOT_DIR = "../static"

# all the different message types
MSG_SOCKET_CONNECT = "wsconnect"
MSG_SOCKET_CLOSE = "wsclose"
MSG_SOCKET_MSG = "wsmsg"  # outgoing message to the Browser
MSG_SOCKET_BROWSER = "wsmsgbrowser"  # incoming message from Browser
MSG_DEBUG_QUERY = "debugquery"  # incoming message from Browser
MSG_INPUT_STRING = "inputstring"  # text written on the remote keyboard
MSG_INPUT_SPECIAL = "inputspecial"  # special key pressed on the remote keyboard, e.g. "enter", "backspace", "up", "down", ...
MSG_SOCKET_xxx = "xxxx"

# all the different query types
QUERY_PLAYLIST = "satipplaylist"

# limits the number of search results when do a query
MAX_QUERY_SIZE = 40
