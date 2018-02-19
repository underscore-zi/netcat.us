from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort, g
from app.config import missions as MISSIONS
from app import mongo
from collections import OrderedDict

module = Blueprint('users', __name__, url_prefix='/users')

@module.route("/name/<name>/")
def profile(name):
    user = mongo.db.users.find_one_or_404({'name':name})

    categories = MISSIONS.get_categories()
    missions = OrderedDict()
    for cat in categories:
        ms = MISSIONS.get_missions(cat)
        missions[cat] = OrderedDict()
        for m in ms:
            missions[cat][m['name']] = m

    return render_template('users/profile.html', user=user, missions=missions, category_titles=categories)

@module.route("/id/<id>/")
def profile_by_id(id):
    user = mongo.db.users.find_one_or_404({"id":id})
    return redirect(url_for('users.profile', name=user['name']))

@module.route("/leaderboard/")
def leaderboard():
    from app.config import ranks
    tmp_ranks = ranks.get_ranks()
    all_ranks = {}
    for r in tmp_ranks: 
        print tmp_ranks[r]
        all_ranks[tmp_ranks[r]['name']] = tmp_ranks[r]
    from pymongo import DESCENDING
    leads = list(mongo.db.users.find({'is_staff':{'$exists':0}}).sort("exp",DESCENDING).limit(10))
    return render_template('users/leaderboard.html', leads=leads, ranks=all_ranks)


@module.route("/ranks/")
def ranks():
    from app.config import ranks
    all_ranks = ranks.get_ranks()
    for r in all_ranks:
        all_ranks[r]['count'] = mongo.db.users.find({"rank":all_ranks[r]['name']}).count()

    return render_template('users/ranks.html', rank_order=reversed(all_ranks), ranks=all_ranks)