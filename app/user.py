import discord
import app
import flask

def get_user_document(uid):
    return app.mongo.db.users.find_one({"id" : uid})

def get_document():
    if flask.g.userinfo == None: return None
    return app.mongo.db.users.find_one({"id" : flask.g.userinfo['id']})

def register(info):
    return app.mongo.db.users.insert({'id': info['id'], "name": info['username'], "rank":"", "exp":0,})

def get_discord():
    return discord.get_me()

def has_account():
    return flask.session.get('oauth2_token', None) != None

def is_staff(userinfo=None):
    if userinfo == None: userinfo = flask.g.userinfo
    return 'is_staff' in userinfo

def get_roles(userinfo=None):
    if userinfo == None: userinfo = flask.g.userinfo
    return discord.get_roles(userinfo['id'])


def complete_challenge(name):
    app.mongo.db.users.update_one({"_id" : flask.g.userinfo['_id'] }, {'$set' : {name.strip():1}})
    flask.g.userinfo[name.strip()] = 1
    _refresh_points(flask.g.userinfo)


''' This will recalculate a user's points and check that they have the right rank.
    Points are recalculated instead of just adding missions points to prevent race
    conditions resulting in too many points being added. 
    force_update will force setting a the discord rank, even if their rank hasn't
    changed'''
def _refresh_points(userinfo, force_update=False):
    import app.config.ranks as ranks
    points = 0
    for key in userinfo:
        m = app.config.missions.get_mission(key)
        if m != None:
            points += int(m['exp'])
    new_rank = ranks.lookup_rank(points)
    if new_rank != None and (force_update or userinfo['rank'] != new_rank['name']):
        discord.update_rank(userinfo['id'], new_rank['name'])
    if new_rank == None: new_rank = ''
    else: new_rank = new_rank['name']
    app.mongo.db.users.update_one({"_id" : userinfo['_id'] }, {'$set' : {'exp':points, 'rank':new_rank}})