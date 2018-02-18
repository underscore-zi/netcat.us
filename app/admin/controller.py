from collections import OrderedDict
import random, re, subprocess, string
from functools import wraps
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort
from app import app
from app.config import missions as MISSIONS

module = Blueprint('admin', __name__, url_prefix='/admin')

OPS_ROLE = '-' #Role requires to have full access to this panel

'''All users trying to access this module must have the is_staff flag set.'''
@module.before_request
def admin_check():
    import app.user as user
    if not user.is_staff(): abort(403)

'''Query discord for user roles with every request to prevent make sure access
   is always accurate'''
@module.before_request
def setup_roles():
    import app.user as user
    roles = user.get_roles()
    g.roles = roles
    app.jinja_env.globals['roles'] = g.roles
    app.jinja_env.globals['IS_OPS'] = check_role(OPS_ROLE)

'''Require CSRF Token for all POST requests'''
@module.before_request
def csrf_check():
    if 'CSRF_TOKEN' not in session: 
        session['CSRF_TOKEN'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    app.jinja_env.globals['CSRF_TOKEN'] = session['CSRF_TOKEN']

    if request.method == "POST":
        token = session.get('CSRF_TOKEN', None)
        if token == None or token != request.form.get('csrf_token'):
            abort(403)

def check_role(role_name):
    return role_name in g.roles

def require_role(role_name):
    if not check_role(role_name):
        abort(403)


'''Displays the state of all the containers'''
@module.route('/containers/')
def view_containers():
    missions = MISSIONS.get_missions()
    containers = OrderedDict()
    for m in MISSIONS.get_missions():
        if 'docker' in missions[m]: 
            containers[m] = missions[m]
            containers[m]['state'] = check_state(containers[m]['name'])
    return render_template('admin/containers.html', containers=containers)

'''Returns the number of running docker instances with the given tag'''
def check_state(tag):
    tag = re.sub('[^0-9a-zA-Z_\-]+', '', tag)
    cmd = "docker ps -q --filter status=running --filter ancestor=%s | wc -l" % (tag)
    try:
        output = subprocess.check_output(cmd, shell=True)
        return int(output.strip())
    except subprocess.CalledProcessError as e:
        flash('Error: Unable to check status of: {} - {}'.format(tag, e.output))
        return 0;

@module.route('/containers/<name>', methods=['POST'])
def container_action(name):
    action = request.form.get('action', None)
    actions = ['Start']
    if check_role(OPS_ROLE):
        actions = ['Start', 'Stop', 'Rebuild']

    if not action in actions: 
        flash('Error: Unknown action ({})'.format(action))
        return redirect(url_for('admin.view_containers'))

    mission = MISSIONS.get_mission(name)
    if not 'docker' in mission:
        flash('Error: No container was found for the "{}" mission.'.format(name))
        return redirect(url_for('admin.view_containers'))

    tag = re.sub('[^0-9a-zA-Z_\-]+', '', mission['name'])
    start_cmd = ''
    if 'ports' in mission and ':' in mission['ports']:
        ports = mission['ports'].split(':')
        start_cmd = "docker run -d -p {}:{} {}:latest".format(ports[1],ports[0], tag)
    else:
        start_cmd = "docker run -d {}".format(tag)

    stop_cmd  = "docker kill $(docker ps -q --filter status=running --filter ancestor={})".format(tag)
    build_cmd = "docker build -t {} \"{}\"".format(tag, mission['docker'])

    cmds = []
    if action == 'Stop':
        cmds.append(stop_cmd)
    elif action == 'Start':
        cmds.append(start_cmd)
    elif action == 'Rebuild':
        cmds.append(stop_cmd)
        cmds.append(build_cmd)
        cmds.append(start_cmd)

    output = "\n"
    for cmd in cmds:
        output += "$ {}\n".format(cmd)
        try:
            o = subprocess.check_output(cmd, shell=True)
            output += o.strip() + "\n"
        except subprocess.CalledProcessError as e:
            output += e.output.strip() + "\n"
    flash(output)
    return redirect(url_for('admin.view_containers'))

    

'''Displays a .config file'''
@module.route('/config/<file>/')
def view_config(file):
    if file == 'missions':
        from app.config import missions
        return render_template('admin/mission_config.html', missions=missions, categories=missions._categories)
    elif file == 'ranks':
        from app.config import ranks
        return render_template('admin/ranks_config.html', ranks=ranks.get_ranks())
    else:
        flash('Unknow config file: {}'.format(file))
        return redirect(url_for('admin.view_containers'))

@module.route('/config/<file>/reload', methods=['POST'])
def reload_config(file):
    require_role(OPS_ROLE)

    if file == 'missions':
        from app.config import missions
        reload(missions)
        flash("Success: Missions config has been reloaded")
    elif file == 'ranks':
        from app.config import ranks
        reload(ranks)
        flash("Success: Ranks config has been reloaded")
    else:
        flash('Unknow config file: {}'.format(file))
        return redirect(url_for('admin.view_containers'))
    
    return redirect(url_for('admin.view_config', file=file))

    

'''Saves changes to the .config'''
@module.route('/config/<file>/edit', methods=['GET'])
def read_raw_config(file):
    require_role(OPS_ROLE)

    if file == 'missions':
        fn = 'missions.config'
    elif file == 'ranks':
        fn = 'ranks.config'
    else:
        flash('Error: Unknown config ({})'.format(file))
        return redirect(url_for('admin.view_containers'))

    with open(app.config['APP_BASE'] + '/config/' + fn, 'r') as fp: 
        content=fp.read()

    return render_template('admin/edit_config.html', filename=file, content=content)

@module.route('/config/<file>/save', methods=['POST'])
def save_config(file):
    require_role(OPS_ROLE)

    if file == 'missions':
        fn = 'missions.config'
    elif file == 'ranks':
        fn = 'ranks.config'
    else:
        flash('Error: Unknown config ({})'.format(file))
        return redirect(url_for('admin.view_containers'))

    content = action = request.form.get('content', None)
    if content == None or content.strip() == '':
        flash('Error: No content.')
        return redirect(url_for('admin.read_raw_config', file=file))

    with open(app.config['APP_BASE'] + '/config/' + fn, 'w') as fp: 
        fp.write(content)

    return reload_config(file)


'''Runs a script out of app/Scripts'''
@module.route('/run/<name>', methods=['POST'])
def run_script(name):
    pass