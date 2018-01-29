from app import app
import configparser
import collections

parser = configparser.ConfigParser()
parser.read(app.config['APP_BASE'] + "/config/missions.config")

_missions = {}
_categories = collections.OrderedDict()

'''Returns the content from msisions.config for the given mission'''
def get_mission(name):
    return _missions.get(name.strip().lower(), None)

'''Get list of missions for a given category'''
def get_missions(category=None):
    if category == None:
        return _missions
    ms = []
    for m in _categories.get(category.strip().lower(), []):
        ms.append(_missions.get(m.strip()))
    return ms

'''Returns the list of categories accounting to the navlinks config'''
def get_categories():
    return _categories.keys()



# Initalize category and mission dictionaries
for cat in parser.get('Navigation', 'navlinks').split(','):
    links =  parser.get(cat, 'links').split(',')
    _categories[cat] = links
    for m in links:
        m = m.strip().lower()
        _missions[m] = {}
        for entry in parser.items(m):
            _missions[m][entry[0]] = entry[1]