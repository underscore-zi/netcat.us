import configparser
from collections import OrderedDict
from app import app

parser = configparser.ConfigParser()
parser.read(app.config['APP_BASE'] + "/config/ranks.config")

_ranks = OrderedDict()

''' Lookup what rank category `points` falls within '''
def lookup_rank(points):
    last = None
    for r in _ranks:
        if points < _ranks[r]['points']: break
        else: last = _ranks[r]
    return last


''' Returns the rank definition matching `name` '''
def get_rank(name):
    return _ranks.get(name.strip().lower(), None)


''' Returns the minimum points necessary for the given `rank` '''
def get_points(rank):
    r = _ranks.get(name.strip().lower(), None)
    if not r: return None
    return r['points']

''' Returns the entire ranks dictionary '''
def get_ranks():
    return _ranks

# Initalize the _ranks dictionary on startup
for rank in parser.sections():
    _ranks[rank] = {}
    for entry in parser.items(rank):
        if entry[0] =='points':
            _ranks[rank][entry[0]] = int(entry[1])
        else:
            _ranks[rank][entry[0]] = entry[1]


