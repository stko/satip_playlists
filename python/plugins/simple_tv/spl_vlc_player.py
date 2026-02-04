#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Standard module
import time
import threading

# Non standard modules (install with pip)
import vlc

# own local modules
from messagehandler import Query
import defaults
from splthread import SplThread
from jsonstorage import JsonStorage


class SplPlugin(SplThread):
    plugin_id = "vlcplayer"
    plugin_names = ["VLC Player"]

    def __init__(self, modref):
        """inits the plugin"""
        self.modref = modref

        # do the plugin specific initialisation first

        self.movielist_storage = JsonStorage(
            self.plugin_id,
            "backup",
            "config.json",
            {},
        )  # set defaults
        self.lock = threading.Lock()  # create a lock, only if necessary

        # at last announce the own plugin
        super().__init__(modref.message_handler, self)
        modref.message_handler.add_event_handler(self.plugin_id, 0, self.event_listener)
        modref.message_handler.add_query_handler(self.plugin_id, 0, self.query_handler)
        self.run_flag = True

        # do any further initialisation here
        self.vlc_instance = vlc.Instance()
        self.player = None
        self.url_toplay = ""

    def event_listener(self, queue_event):
        """try to send simulated answers"""
        print("VLC player event handler", queue_event.type, queue_event.user)
        if (
            queue_event.type == defaults.MSG_SOCKET_BROWSER
        ):  # the websocket has got a query from the websocket
            browser_message = queue_event.data
            print("browser message:", browser_message)
            msg_type = browser_message.get("type", "")
            msg_data = browser_message.get("config", {})
            if msg_type == "tvcontrol_play_station":
                with self.lock:
                    self.url_toplay = msg_data.get("url", "")
                """
                self.modref.message_handler.queue_event(
                    queue_event.user,
                    defaults.MSG_SOCKET_MSG,
                    {"type": "tvcontrol_list_response", "config": browser_message},
                )
                """
        # for further pocessing, do not forget to return the queue event
        return queue_event

    def query_handler(self, queue_event, max_result_count) -> list:
        # print("satipplaylists handler query handler",queue_event.type, queue_event.user, max_result_count, queue_event.params)
        if queue_event.type == defaults.MESSAGE_XXXX:  # wait for defined messages
            pass
        return []

    def _run(self):
        """starts the server"""
        while self.run_flag:
            time.sleep(0.5)
            with self.lock:
                # as https://github.com/blacklight/platypush/commit/833f810d4b14bbd9ee967a9ef3642aa0f6f9ced2 stated:
                # VLC is not thread safe, so we have to ensure that all calls to VLC are done from the same thread
                if self.url_toplay:
                    if self.player is None:
                        self.player = self.vlc_instance.media_player_new()
                    else:
                        self.player.stop()
                        # self.player.set_pause(1)  # pause current playback
                        # time.sleep(0.2)
                    media = self.vlc_instance.media_new(self.url_toplay)
                    self.player.set_media(media)
                    media.release()
                    self.player.play()
                    self.url_toplay = ""

    def _stop(self):
        self.run_flag = False

    # ------ plugin specific routines
