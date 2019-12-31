from mycroft import MycroftSkill, intent_file_handler


class Webplay(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('webplay.intent')
    def handle_webplay(self, message):
        self.speak_dialog('webplay')


def create_skill():
    return Webplay()

