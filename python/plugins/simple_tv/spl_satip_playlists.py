#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Standard module
import json
import time
import requests
from messagehandler import Query
import defaults
from splthread import SplThread
from jsonstorage import JsonStorage
import threading

# Non standard modules (install with pip)

# ScriptPath = os.path.realpath(os.path.join(
# 	os.path.dirname(__file__), "./common"))


# Add the directory containing your module to the Python path (wants absolute paths)
# ys.path.append(os.path.abspath(ScriptPath))
# own local modules


class SplPlugin(SplThread):
    plugin_id = "satipplaylists"
    plugin_names = ["SatIP Playlists"]

    def __init__(self, modref):
        """inits the plugin"""
        self.modref = modref

        # do the plugin specific initialisation first

        self.movielist_storage = JsonStorage(
            self.plugin_id,
            "backup",
            "config.json",
            {
                "sources": [
                    "https://raw.githubusercontent.com/dersnyke/satipplaylists/main/satip_astra192e.m3u"
                ],
                "playlists": {
                    "wohnzimmer": {
                        "replaces": [{"from": "rtsp:", "to": "http:"}],
                        "adds": [
                            "#KODIPROP:inputstreamclass=inputstream.ffmpegdirect",
                            "#KODIPROP:inputstream.ffmpegdirect.mime_type=video/mp2t",
                        ],
                        "stations": ["DMAX"],
                    }
                },
            },
        )  # set defaults
        self.stations = {}
        self.last_update = 0
        self.lock = threading.Lock()  # create a lock, only if necessary

        # at last announce the own plugin
        super().__init__(modref.message_handler, self)
        modref.message_handler.add_event_handler(self.plugin_id, 0, self.event_listener)
        modref.message_handler.add_query_handler(self.plugin_id, 0, self.query_handler)
        self.runFlag = True

    def event_listener(self, queue_event):
        """try to send simulated answers"""
        # print("uihandler event handler", queue_event.type, queue_event.user)
        if queue_event.type == defaults.MSG_SOCKET_xxx:
            pass
        if queue_event.type == "_join":
            print("a web client has connected", queue_event.data)
        # for further pocessing, do not forget to return the queue event
        return queue_event

    def query_handler(self, queue_event, max_result_count):
        # print("satipplaylists handler query handler", queue_event.type,  queue_event.user, max_result_count)
        if queue_event.type == defaults.QUERY_PLAYLIST:  # wait for defined messages
            name = queue_event.params.lower()
            sources = self.movielist_storage.read("sources", [])
            playlists = self.movielist_storage.read("playlists", [])
            if name == "stations":  # return
                stations = self.collect_urls(sources)
                station_names = list(stations.keys())
                station_names.sort()
                return [json.dumps({"stations": station_names}, indent=4)]
            elif name == "all":  # return
                stations = self.collect_urls(sources)
                final_m3u = self.format_m3u(stations, {})
                return [final_m3u]
            elif name in playlists:
                stations = self.collect_urls(sources)
                final_m3u = self.playlist(stations, playlists[name])
                return [final_m3u]
        return ["unknown playlist"]

    def _run(self):
        """starts the server"""
        while self.runFlag:
            time.sleep(10)
            with self.lock:
                pass

    def _stop(self):
        self.runFlag = False

    # ------ plugin specific routines

    def collect_urls(self, sources: list) -> dict:
        new_stations = {}
        if self.stations and (time.time() - self.last_update) < 3600:  # 1 hour cache
            return self.stations
        self.last_update = time.time()
        for source in sources:
            r = requests.get(source)

            print("Status Code:")
            print(r.status_code)
            if r.status_code != 200:
                continue

            station = ""
            name = ""
            # print (r.text)
            lines = r.text.split("\n")
            for line in lines:
                line = line.strip()
                if line[:1] == "#":
                    # print(line)
                    elements = line.split(",", 1)
                    if len(elements) < 2:
                        continue
                    name = elements[1].strip().lower()
                    station = line
                else:
                    url = line
                    stations[name] = {"station": station, "url": url}
            return stations

    def playlist(self, stations: dict, playlist_data: hash) -> str:
        filtered_stations = {}
        for name in playlist_data["stations"]:
            name = name.lower()
            if name in stations:
                filtered_stations[name] = stations[name]
        return self.format_m3u(filtered_stations, playlist_data)

    def format_m3u(self, stations: dict, playlist_data: hash) -> str:
        new_m3u = ["#EXTM3U"]
        for station_data in stations.values():
            url = station_data["url"]
            if "replaces" in playlist_data:
                for replace in playlist_data["replaces"]:
                    url = url.replace(replace["from"], replace["to"])
            if "adds" in playlist_data:
                new_m3u += playlist_data["adds"]

            new_m3u += [station_data["station"], url]
        final_m3u = "\n".join(new_m3u)
        return final_m3u
