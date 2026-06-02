#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Standard module

# Source - https://stackoverflow.com/a/16682549
# Posted by Treviño, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-01, License - CC BY-SA 4.0

import subprocess
import time

# Non standard modules (install with pip)

# own local modules
from messagehandler import Query
import defaults
from splthread import SplThread
from jsonstorage import JsonStorage


class SplPlugin(SplThread):
    plugin_id = "cec"
    plugin_names = ["CEC Control"]

    def __init__(self, modref):
        """inits the plugin"""
        self.modref = modref

        # do the plugin specific initialisation first

        self.configuration = JsonStorage(
            self.plugin_id,
            "backup",
            "config.json",
            {
                "device": "TV",
            },
        )  # set defaults
        self.tv_on = False
        # self.lock = threading.Lock()  # create a lock, only if necessary

        # at last announce the own plugin
        super().__init__(modref.message_handler, self)
        modref.message_handler.add_event_handler(self.plugin_id, 0, self.event_listener)
        modref.message_handler.add_query_handler(self.plugin_id, 0, self.query_handler)
        self.run_flag = True

        # do any further initialisation here

    def event_listener(self, queue_event):
        print(
            "CEC Control event handler",
            queue_event.type,
            queue_event.user,
            queue_event.data,
        )
        if queue_event.type == defaults.MSG_INPUT_SPECIAL:
            input_special = queue_event.data
            print("Received special input:", input_special)
            # Process the special input power on/off and toggle the TV state
            if input_special == "power":
                if self.tv_on:
                    self.modref.message_handler.queue_event(
                        None,
                        defaults.MSG_TVCONTROL_POWER_OFF,
                        None,
                    )
                    self.send_command("standby 0")
                    self.tv_on = False
                    print("Turning TV off")
                else:
                    self.modref.message_handler.queue_event(
                        None,
                        defaults.MSG_TVCONTROL_POWER_ON,
                        None,
                    )
                    self.send_command("on 0")
                    self.tv_on = True
                    print("Turning TV on")

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
    def send_command(self, cmd: str) -> str:
        # following the example from https://gist.github.com/rmtsrc/dc35cd1458cd995631a4f041ab11ff74

        # Run 'echo "scan"' and pipe the output to 'cec-client'
        ps_cmd = subprocess.Popen(["echo", cmd], stdout=subprocess.PIPE)

        # Run 'cec-client' and pipe the output of 'echo' to it
        head_cmd = subprocess.Popen(
            ["cec-client", "-s", "-d", "1"],
            stdin=ps_cmd.stdout,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )

        stdout, stderr = head_cmd.communicate()
        return stdout
