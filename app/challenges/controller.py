from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort
from app.config import missions as MISSIONS
from app import user

module = Blueprint('challenges', __name__, url_prefix='/challenges')

@module.route("/<category>/<name>/")
@module.route("/<category>/")
@module.route("/")
def view_category(category='web', name=None):
    from app import mongo

    if name != None and MISSIONS.get_mission(name) == None:
        flash("Error: Unknown mission({})".format(name))
        return redirect(url_for('challenges.view_category', category=category))

    tmp_ms = MISSIONS.get_missions(category)
    if not tmp_ms: 
        flash('Error: Unknown category ({})'.format(category))
        return redirect(url_for('challenges.view_category', category='web'))

    ms = []
    for m in tmp_ms:
        m['solves'] = mongo.db.users.find({ m['name'] : {'$exists': 1} }).count()
        m['solved'] = g.userinfo != None and m['name'] in g.userinfo
        ms.append(m)

    return render_template('challenges/list.html', missionName=name, categories=MISSIONS.get_categories(), active_category=category, missionDetails=ms)

@module.route("/<category>/<name>/", methods=['POST'])
def submit(category, name):
    from app import mongo
    userinfo = g.userinfo
    if userinfo == None:
        flash("Error: You must be logged in to submit flags.")
        return redirect(url_for('challenges.view_category', category=category))

    mission = MISSIONS.get_mission(name)
    if mission == None:
        flash("Error: Unknown mission ({})".format(name))
        return redirect(url_for('challenges.view_category', category=category))

    if name in userinfo:
        flash("Error: You have already completed this mission.")
        return redirect(url_for('challenges.view_category', category=category))

    flag = request.form.get('flag', None)
    if flag == None or flag=='':
        flash("Error: You must provide a flag.")
        return redirect(url_for('challenges.view_category', category=category, name=name))

    if flag != mission['flag']:
        flash("Error: Incorrect flag.")
        return redirect(url_for('challenges.view_category', category=category, name=name))

    user.complete_challenge(name)
    flash('Congratulations! You have been awarded {} points!'.format(mission['exp']))
    return redirect(url_for('challenges.view_category', category=category))


