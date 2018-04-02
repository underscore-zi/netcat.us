from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort, g, jsonify
from app.config import missions as MISSIONS
from app import mongo
from collections import OrderedDict
import json


module = Blueprint('users', __name__, url_prefix='/users')

def display_profile(user,api=False):
    categories = MISSIONS.get_categories()
    missions = OrderedDict()
    for cat in categories:
        ms = MISSIONS.get_missions(cat)
        missions[cat] = OrderedDict()
        for m in ms:
            missions[cat][m['name']] = m
    if api:
        if '_id' in user: del user['_id']
        return jsonify(user)
    return render_template('users/profile.html', user=user, missions=missions, category_titles=categories)

@module.route("/name/<name>/")
def profile(name,api=False):
    user = mongo.db.users.find_one_or_404({'name':name})
    return display_profile(user,api)

@module.route("/id/<id>/")
def profile_by_id(id,api=False):
    user = mongo.db.users.find_one_or_404({"id":id})
    return display_profile(user,api)

@module.route("/leaderboard/")
def leaderboard(api=False):
    from app.config import ranks
    tmp_ranks = ranks.get_ranks()
    all_ranks = {}
    for r in tmp_ranks: 
        print tmp_ranks[r]
        all_ranks[tmp_ranks[r]['name']] = tmp_ranks[r]
    from pymongo import DESCENDING
    leads = list(mongo.db.users.find({'is_staff':{'$exists':0}}).sort("exp",DESCENDING).limit(10))
    staff = list(mongo.db.users.find({'is_staff':{'$exists':1}}).sort("exp",DESCENDING))
    
    if api:
        resp_l = []
        for l in leads:
            resp_l.append({
                'id':l['id'],
                'name':l['name'],
                'rank':l['rank'],
                'exp':l['exp'],
            })
        resp_s = []
        for l in staff:
            resp_s.append({
                'id':l['id'],
                'name':l['name'],
                'rank':l['rank'],
                'exp':l['exp'],
            })
        return jsonify({"leaderboard":resp_l,"staff":resp_s})

    return render_template('users/leaderboard.html', leads=leads, staff=staff, ranks=all_ranks)


@module.route("/ranks/")
def ranks(api=False):
    from app.config import ranks
    all_ranks = ranks.get_ranks()
    for r in all_ranks:
        all_ranks[r]['count'] = mongo.db.users.find({"rank":all_ranks[r]['name']}).count()

    if api:
        if '_id' in all_ranks: del all_ranks['_id']
        return jsonify({"ranks":all_ranks,"rank_order":all_ranks.keys()})

    return render_template('users/ranks.html', rank_order=reversed(all_ranks), ranks=all_ranks)