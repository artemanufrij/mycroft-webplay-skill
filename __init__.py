import os
import subprocess
import requests

from adapt.intent import IntentBuilder

from urllib.parse import quote

from mycroft import intent_file_handler, intent_handler
from mycroft.audio import wait_while_speaking
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel

host = "http://localhost:31204/"


class Webplay(CommonPlaySkill):
    def __init__(self):
        super().__init__(name="WebplaySkill")

    def CPS_match_query_phrase(self, phrase):
        return None

    def CPS_start(self, phrase, data):
        url = data['track']
        self.audioservice.play(url)

    @intent_file_handler('Random.intent')
    def handle_random_play(self, message):
        self.speak_dialog("random")

    @intent_file_handler('Radio.intent')
    def handle_radio_play(self, message):
        self.speak_dialog("random")
        url = host + "api/radio/"
        r = requests.get(url)
        try:
            response = r.json()
            self.play_tracks(response)

        except:
            self.speak_dialog("nothing.found")

    @intent_handler(IntentBuilder("").require("Album").require("AlbumTitle"))
    def handler_album_play(self, message):
        self.speak_dialog("album")
        url = host + "api/album/" + \
            message.data.get("AlbumTitle")

        r = requests.get(url)
        try:
            response = r.json()
            self.play_tracks(response)

        except:
            self.speak_dialog("nothing.found")

    def play_track(self, id):
        url = host + "api/track/" + id + "/stream/128"
        wait_while_speaking()
        self.audioservice.play(url)

    def play_tracks(self, parent):
        tracks = []
        for track in parent["tracks"]:
            tracks.append(host + "api/track/" + track["_id"] + "/stream/128")
        wait_while_speaking()
        self.audioservice.play(tracks)

    @intent_file_handler('Stop.intent')
    def handle_stop_playing(self, message):
        self.stop()

    @intent_file_handler('NextTrack.intent')
    def next_track(self, message):
        self.audioservice.next()


def create_skill():
    return Webplay()
