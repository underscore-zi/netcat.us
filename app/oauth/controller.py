from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort, Markup
from requests_oauthlib import OAuth2Session
import os
from app import app, user, discord as discord_api

module = Blueprint('oauth', __name__, url_prefix='/oauth')

@module.route('/callback')
def callback():
    if request.values.get('error'):
        return Markup.escape(request.values['error'])

    discord = discord_api.make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        app.config['DISCORD_API_URL'] + discord_api.TOKEN_PATH,
        client_secret=app.config['OAUTH2_CLIENT_SECRET'],
        authorization_response=request.url)
    discord_api.token_updater(token)

    info = discord_api.get_me()
    if info == None:
        flash("Error: Could not authenticate with discord.")
        return redirect(url_for('home'))

    userinfo = user.get_user_document(info['id'])
    if userinfo == None:
        user.register(info)
        flash("You have been registered.")
    else: 
        flash("You have been logged in.")
        user._refresh_points(userinfo, force_update=True)

    return redirect(url_for('home'))

@module.route('/login')
def login():
    if user.has_account():
        info = user.get_discord()
        if info != None and user.get_user_document(info['id']) != None:
            return redirect(url_for('home'))
    app.config['OAUTH2_REDIRECT_URI'] = 'http://{}/callback'.format(request.headers.get('Host', ''))
    return redirect(discord_api.generate_auth_url())

@module.route('/logout')
def logout():
    session.pop('oauth2_token')
    flash('You have been signed out.')
    return redirect(url_for('home'))
