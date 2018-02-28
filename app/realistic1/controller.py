from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort
module = Blueprint('realistic1', __name__, url_prefix='/drone')


@module.route('/')
def drone():
    return render_template('realistic1/drone.html')

@module.route('/dronepage')
def dronepage():
    person = {'name':"NULL", 'secret':"aG9yc2VzaGl0DQo="}
    passdrone = ""
    if request.args.get('name'):
        person['name'] = request.args.get('name')
    if person['name'] == "{{person.secret}}":
        passdrone = "aG9yc2VzaGl0DQo="
    elif '{{' in person['name'] and '}}' in person['name']:
        # Adding this hint because natural target would be a pop a shell, not grab a var
        passdrone = "Right idea, but we had to sandbox this challenge. Try just getting the secret..."
    if session.get('realistic1_logged_in', None) is None:
        return render_template("realistic1/login.html", passdrone=passdrone)
    else:
        flash(u'Drone Package ControlPanel', 'success')
        return render_template("realistic1/table.html")

@module.route('/dronelogin', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'horseshit' and request.form['username'] == 'dronedelivery12':
        session['realistic1_logged_in'] = True
    else:
        flash(u'Error: Wrong password!', 'danger')
    return dome()

@module.route('/dronelogout')
def do_logout():
    session.pop('realistic1_logged_in', None)
    return redirect(url_for('realistic1.dronepage'))

def dome():
    if not session.get('realistic1_logged_in'):
        return render_template('realistic1/login.html')
    else:
        return dronepage()
