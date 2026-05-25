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
    plugin_id = "remotekbd"
    plugin_names = ["Remote Keyboard"]

    def __init__(self, modref):
        """inits the plugin"""
        self.modref = modref

        # do the plugin specific initialisation first

        self.configuration = JsonStorage(
            self.plugin_id,
            "backup",
            "config.json",
            {
                "input_device": "/dev/input/by-id/usb-USB_Composite_Device_USB_Composite_Device_0001-event-kbd",
                "input_delay": 1,
            },
        )  # set defaults
        # open input device in binary mode
        """
        FORMAT represents the format used by linux kernel input event struct
        See https://github.com/torvalds/linux/blob/v5.5-rc5/include/uapi/linux/input.h#L28
        Stands for: long int, long int, unsigned short, unsigned short, unsigned int
        """
        self.FORMAT = "llHHI"
        self.EVENT_SIZE = struct.calcsize(self.FORMAT)
        self.keymap = {}
        with open(os.path.join(os.path.dirname(__file__), "keyconfig.json"), "r") as f:
            key_config = json.load(f)
            for key, value in key_config.items():
                keycode = int(key)
                if value.get("isascii", False):
                    charlist = value.get("key", "")
                    for i in range(len(charlist)):
                        self.keymap[keycode + i] = {"isascii": True, "key": charlist[i]}
                else:
                    self.keymap[keycode] = {"isascii": False, "key": value["key"]}
        # open file in binary mode
        self.in_file = None
        self.event = None
        try:
            self.in_file = open(self.configuration.read("input_device"), "rb")
            os.set_blocking(self.in_file.fileno(), False)
            self.event = self.in_file.read(self.EVENT_SIZE)
        except Exception as e:
            print(f"Error occurred while opening input device: {e}")
        self.time_ticker = time.time()
        self.input_buffer = ""
        # self.lock = threading.Lock()  # create a lock, only if necessary

        # at last announce the own plugin
        super().__init__(modref.message_handler, self)
        modref.message_handler.add_event_handler(self.plugin_id, 0, self.event_listener)
        modref.message_handler.add_query_handler(self.plugin_id, 0, self.query_handler)
        self.run_flag = True

        # do any further initialisation here

    def event_listener(self, queue_event):

        # for further pocessing, do not forget to return the queue event
        return queue_event

    def query_handler(self, queue_event, max_result_count) -> list:
        # print("satipplaylists handler query handler",queue_event.type, queue_event.user, max_result_count, queue_event.params)
        if queue_event.type == defaults.MSG_SOCKET_xxx:  # wait for defined messages
            pass
        return []

    def _run(self):
        """starts the server"""
        input_delay = self.configuration.read("input_delay", 1)
        while self.run_flag:
            if self.event and len(self.event) == self.EVENT_SIZE:
                tv_sec, tv_usec, event_type, code, value = struct.unpack(
                    self.FORMAT, self.event
                )

                if event_type != 0 or code != 0 or value != 0:
                    """
                    print(
                        "Event type %u, code %u, value %u at %d.%d"
                        % (event_type, code, value, tv_sec, tv_usec)
                    )
                    """
                    if event_type == 1 and value == 1:  # EV_KEY and Key_down?
                        if code in self.keymap:
                            key_info = self.keymap[code]
                            if key_info["isascii"]:
                                # print(key_info["key"], end="", flush=True)
                                self.input_buffer += key_info["key"]
                                self.time_ticker = time.time()
                            else:
                                # print("code %u" % code)
                                print("\nspecial: " + key_info["key"], flush=True)
                                self.modref.message_handler.queue_event(
                                    None,
                                    defaults.MSG_INPUT_SPECIAL,
                                    key_info["key"],
                                )
                    else:
                        pass  # print("code %u" % code)
                else:
                    # Events with code, type and value == 0 are "separator" events
                    pass  # print("===========================================")
            else:
                time.sleep(0.1)  # avoid busy waiting
            if time.time() - self.time_ticker > input_delay:
                self.time_ticker = time.time()
                if self.input_buffer:
                    print("\nBuffered input:", self.input_buffer)
                    self.modref.message_handler.queue_event(
                        None,
                        defaults.MSG_INPUT_STRING,
                        self.input_buffer,
                    )
                    self.input_buffer = ""
            if self.in_file:
                self.event = self.in_file.read(self.EVENT_SIZE)
        if self.in_file:
            self.in_file.close()

    def _stop(self):
        self.run_flag = False

    # ------ plugin specific routines
