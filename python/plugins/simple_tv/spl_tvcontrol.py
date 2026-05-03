#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Standard module

# Source - https://stackoverflow.com/a/16682549
# Posted by Treviño, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-01, License - CC BY-SA 4.0

import os
import struct
import time
import json

# Non standard modules (install with pip)

# own local modules
from messagehandler import Query
import defaults
from splthread import SplThread
from jsonstorage import JsonStorage
import threading


class SplPlugin(SplThread):
    plugin_id = "tvcontrol"
    plugin_names = ["TV Control"]

    def __init__(self, modref):
        """inits the plugin"""
        self.modref = modref

        # do the plugin specific initialisation first

        self.configuration = JsonStorage(
            self.plugin_id,
            "backup",
            "config.json",
            {
                "room": "wohnzimmer",
            },
        )  # set defaults
        self.playlist = []
        self.videotext = 0
        self.channel = 0
        self.num_channels = 0
        # self.lock = threading.Lock()  # create a lock, only if necessary

        # at last announce the own plugin
        super().__init__(modref.message_handler, self)
        modref.message_handler.add_event_handler(self.plugin_id, 0, self.event_listener)
        modref.message_handler.add_query_handler(self.plugin_id, 0, self.query_handler)
        self.run_flag = True

        # do any further initialisation here

    def event_listener(self, queue_event):
        print(
            "TV Control event handler",
            queue_event.type,
            queue_event.user,
            queue_event.data,
        )
        if queue_event.type == defaults.MSG_INPUT_STRING:
            input_num = 0
            try:
                input_str = queue_event.data
                print("Received input string:", input_str)
                # Process the input string as needed
                input_num = int(
                    input_str
                )  # convert to zero-based index, assuming input is 1-based
                print("Converted input to number:", input_num)
            except Exception as e:
                print("Error processing input string:", e)
                return queue_event
            if not self.videotext:
                self.switch_station(input_num)
            else:
                self.switch_videotext_page(input_num)
        if queue_event.type == defaults.MSG_INPUT_SPECIAL:
            input_special = queue_event.data
            print("Received special input:", input_special)
            # Process the special input as needed, e.g. switch to videotext mode on "enter" key
            if input_special == "videotext":
                if not self.videotext:
                    self.videotext = 100
                    print("Switched to videotext mode")
                else:
                    self.videotext = 0
                    print("Switched to normal mode")
                    self.videotext = 0
                self.switch_videotext_page(self.videotext)
            if input_special == "right":
                if self.videotext:
                    self.videotext += 1
                    print("Switched to next videotext page:", self.videotext)
                    self.switch_videotext_page(self.videotext)
                else:
                    self.channel += 1
                    if self.channel > self.num_channels:
                        self.channel = 1
                    print("Switched to next channel:", self.channel)
                    self.switch_station(self.channel)

            if input_special == "left":
                if self.videotext:
                    if self.videotext > 100:
                        self.videotext -= 1
                        print("Switched to previous videotext page:", self.videotext)
                        self.switch_videotext_page(self.videotext)
                else:
                    self.channel -= 1
                    if self.channel < 1:
                        self.channel = self.num_channels
                    print("Switched to previous channel:", self.channel)
                    self.switch_station(self.channel)

        # for further pocessing, do not forget to return the queue event
        return queue_event

    def query_handler(self, queue_event, max_result_count) -> list:
        # print("satipplaylists handler query handler",queue_event.type, queue_event.user, max_result_count, queue_event.params)
        if queue_event.type == defaults.MSG_SOCKET_xxx:  # wait for defined messages
            pass
        return []

    def _run(self):
        """starts the server"""
        while self.run_flag:
            time.sleep(0.1)

    def _stop(self):
        self.run_flag = False

    # ------ plugin specific routines

    def switch_station(self, input_num):
        input_num = (
            input_num - 1
        )  # convert to zero-based index, assuming input is 1-based
        query = Query(
            None,
            defaults.QUERY_PLAYLIST,
            {
                "name": self.configuration.read("room", "wohnzimmer"),
                "format": "json",
            },
        )
        self.playlist = self.modref.message_handler.query(query)
        if self.playlist and isinstance(self.playlist, list):
            self.num_channels = len(
                self.playlist[0]
            )  # assuming the playlist is a list of dicts
            if (
                0
                <= input_num
                < self.num_channels  # the query result is a list of results, we need the first one, which should be the playlist, and check if the input number is within the range of the playlist
            ):
                self.channel = (
                    input_num + 1
                )  # store the current channel, convert back to one-based index for display
                station_name = list(self.playlist[0].keys())[input_num]
                station = self.playlist[0][
                    station_name
                ]  # get the station at the index of the input number
                print("Selected station:", station)
                self.modref.message_handler.queue_event(
                    None,
                    defaults.MSG_TVCONTROL_PLAY_STATION,
                    {"url": station.get("url", "")},
                )

    def switch_videotext_page(self, input_num):
        print("Switching to videotext page:", input_num)
        # Implement the logic to switch to the specified videotext page here
        # This is a placeholder implementation and should be replaced with actual logic to control the TV's videotext functionality
        self.videotext = input_num
        self.modref.message_handler.queue_event(
            None,
            defaults.MSG_TVCONTROL_SWITCH_VIDEOTEXT_PAGE,
            {"page": input_num},
        )
