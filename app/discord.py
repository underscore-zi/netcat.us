from flask import session
from requests_oauthlib import OAuth2Session
import requests
from app import app

TOKEN_PATH = '/oauth2/token'
ROLES = {}

def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=app.config['OAUTH2_CLIENT_ID'],
        token=token,
        state=state,
        scope=scope,
        redirect_uri=app.config['OAUTH2_REDIRECT_URI'],
        auto_refresh_kwargs={
            'client_id': app.config['OAUTH2_CLIENT_ID'],
            'client_secret': app.config['OAUTH2_CLIENT_SECRET'],
        },
        auto_refresh_url=app.config['DISCORD_API_URL'] + TOKEN_PATH,
        token_updater=token_updater)

def token_updater(token):
    session['oauth2_token'] = token

def generate_auth_url():
    discord = make_session(scope=['identify','email'])
    authorization_url, state = discord.authorization_url(app.config['DISCORD_API_URL'] + '/oauth2/authorize')
    session['oauth2_state'] = state
    return authorization_url

'''Returns the information from an /users/@me query, or None'''
def get_me():
    tk = token=session.get('oauth2_token', None)
    if tk == None: return None
    discord = make_session(token=tk)

    user = discord.get(app.config['DISCORD_API_URL'] + '/users/@me').json()
    if not 'id' in user:
        return None
    return user

# ################################## #
# Start of Discord Bot API functions #
# ################################## #
HEADERS = {'user-agent': 'DiscordBot (netcat.us, 0.01)', 'Authorization':'Bot '+ app.config['BOT_TOKEN']}
def _get(endpoint):
    res = requests.get(app.config['DISCORD_API_URL'] + endpoint, headers=HEADERS)
    return res.json()

def _put(endpoint, data=None):
    h = HEADERS
    if data != None: h['Content-Type'] = 'application/json'
    res = requests.put(app.config['DISCORD_API_URL'] + endpoint, data=data, headers=h)

def _delete(endpoint):
    res = requests.put(app.config['DISCORD_API_URL'] + endpoint, headers=HEADERS)

def _patch(endpoint, data=None):
    h = HEADERS
    if data != None: h['Content-Type'] = 'application/json'
    res = requests.patch(app.config['DISCORD_API_URL'] + endpoint, data=data, headers=h)

def has_role(user_id, role_ids):
    roles = _get('/guilds/{}/members/{}'.format(app.config['GUILD_ID'],user_id))['roles']

    if type(role_ids) is list:
        for role in role_ids:
            if role in roles: return True
        return False
    else:
        return role_ids in roles

def get_roles(user_id):
    res = _get('/guilds/{}/members/{}'.format(app.config['GUILD_ID'],user_id))
    if not 'roles' in res: return []
    roles = []
    for rid in res['roles']:
        roles.append(ROLE_IDS[rid])
    return roles

def set_role(user_id, role_id):
    res = _put('/guilds/{}/members/{}/roles/{}'.format(app.config['GUILD_ID'], user_id, role_id))

def unset_role(user_id, role_id):
    res = _delete('/guilds/{}/members/{}/roles/{}'.format(app.config['GUILD_ID'], user_id, role_id))


def update_rank(uid,rank_name):
    import app.config.ranks as ranks
    
    #Calculate which ranks need to be set and which shouldn't be set
    passed = False
    set_ranks = []
    unset_ranks = []
    all_ranks = ranks.get_ranks()
    for r in all_ranks:
        if passed: unset_ranks.append(all_ranks[r]['role'])
        else: set_ranks.append(all_ranks[r]['role'])
        if all_ranks[r]['name'] == rank_name: passed = True


    #Generate list of new roles taking into account new rank and existing roles
    has_roles = get_roles(uid)
    patch_roles = set_ranks
    for r in has_roles:
        if not r in unset_ranks and not r in patch_roles:
            patch_roles.append(r)

    #Create JSON for PATCH req
    patch_data = ''
    for r in patch_roles:
        patch_data += '"{}",'.format(ROLES[r])
    patch_data = '{"roles":[%s]}'%(patch_data[:-1])
    _patch('/guilds/{}/members/{}'.format(app.config['GUILD_ID'], uid), data=patch_data)

def initalize_roles():
    if ROLES: return
    all_roles = _get('/guilds/%s/roles'%(app.config['GUILD_ID']))
    roles = {}
    role_ids = {}
    for r in all_roles:
        roles[r['name']] = r['id']
        role_ids[r['id']] = r['name']
    return (roles,role_ids)


ROLES, ROLE_IDS = initalize_roles()

