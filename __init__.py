import os
import subprocess
import requests

from adapt.intent import IntentBuilder

from urllib.parse import quote

from mycroft import intent_file_handler, intent_handler
from mycroft.audio import wait_while_speaking
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.util import get_cache_directory
from mycroft.util.parse import match_one

mime = 'audio/mpeg'
host = "http://localhost:31204/"


class Webplay(CommonPlaySkill):
    def __init__(self):
        super().__init__(name="WebplaySkill")
        self.curl = None
        self.now_playing = None
        self.STREAM = '{}/stream'.format(get_cache_directory('WebplaySkill'))

    def CPS_match_query_phrase(self, phrase):
        return None

    def CPS_start(self, phrase, data):
        url = data['track']
        self.audioservice.play(url)

    @intent_file_handler('Stop.intent')
    def handle_stop_playing(self, message):
        self.stop()

    @intent_file_handler('Random.intent')
    def handle_random_play(self, message):
        self.speak_dialog("random")

    @intent_handler(IntentBuilder("").require("Album").
                    require("AlbumTitle"))
    def handler_album_play(self, message):
        self.speak_dialog("album")
        url = host + "api/album/" + \
            message.data.get("AlbumTitle")

        r = requests.get(url)
        try:
            response = r.json()
            track_id = response["tracks"][0]["_id"]
            self.play_track_id(track_id)
        except:
            self.speak_dialog("nothing.found")

    def play_track_id(self, id):
        url = host + "api/track/" + id + "/stream/128"
        print(url)

        #if os.path.exists(self.STREAM):
        #    os.remove(self.STREAM)
        #os.mkfifo(self.STREAM)

        #args = ['curl',
        #        '-L', quote(url, safe=":/"), '-o', self.STREAM]
        #self.curl = subprocess.Popen(args)

        wait_while_speaking()
        # self.CPS_play(('file://' + self.STREAM, mime))
        self.audioservice.play(url)


def create_skill():
    return Webplay()
