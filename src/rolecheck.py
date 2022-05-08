import urllib.request
import json
import config

CHANNEL = config.bot['channel']

with urllib.request.urlopen(f'http://tmi.twitch.tv/group/user/{CHANNEL}/chatters') as response:
    res = json.loads(response.read())

class UserRole:
    def __init__(self, user):
        self.user = user
        
    def ismod(self):
        try:
            if self.user in res['chatters']['moderators']:
                return True
            else:
                return False
        except:
            return False

    def isglobalmod(self):
        try:
            if self.user in res['chatters']['global_mods']:
                return True
            else:
                return False
        except:
            return False

    def isstaff(self):
        try:
            if self.user in res['chatters']['staff']:
                return True
            else:
                return False
        except:
            return False

    def isadmin(self):
        try:
            if self.user in res['chatters']['admins']:
                return True
            else:
                return False
        except:
            return False

    def ishost(self):
        if self.user == CHANNEL:
            return True
        else:
            return False