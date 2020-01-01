import os
import subprocess

from urllib.parse import quote

from mycroft import intent_file_handler
from mycroft.audio import wait_while_speaking
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.util import get_cache_directory
from mycroft.util.parse import match_one

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

    @intent_file_handler('Random.intent')
    def handle_random_play(self, message):
        self.now_playing = True
        self.speak_dialog("random")
        url = "https://wiki.anufrij.de/api/track/5e0b843a95a6e4c6b25d40a8/stream/128"
        mime = 'audio/mpeg'

        if os.path.exists(self.STREAM):
            os.remove(self.STREAM)
        os.mkfifo(self.STREAM)

        self.log.debug('Running curl {}'.format(url))
        args = ['curl', '-L', quote(url, safe=":/"), '-o', self.STREAM]
        self.curl = subprocess.Popen(args)

        wait_while_speaking()
        self.CPS_play(('file://' + self.STREAM, mime))

    @intent_file_handler('Stop.intent')
    def handle_stop_playing(self, message):
        if self.now_playing == True:
            self.stop()
        self.now_playing = False


def create_skill():
    return Webplay()
