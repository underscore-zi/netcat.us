from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort, g
import json


import app.users.controller as users_module



module = Blueprint('api', __name__, url_prefix='/api')

@module.route("/users/name/<name>/")
def profile(name,api=False):
	return users_module.profile(name,True)

@module.route("/users/id/<id>/")
def profile_by_id(id,api=False):
	return users_module.profile_by_id(id,True)

@module.route("/users/leaderboard/")
def leaderboard():
	return users_module.leaderboard(True)

@module.route("/users/ranks/")
def ranks(api=False):
	return users_module.ranks(True)


