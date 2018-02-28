from flask import Flask, render_template, redirect, url_for, g,request
from flask_pymongo import PyMongo
import datetime
app = Flask(__name__)

# To overload default config point NETCAT_CONFIG_FILE to another config file
app.config.from_object('app.config.default')
app.config.from_envvar('NETCAT_CONFIG_FILE', silent=False)

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "200 per hour"]
)

# Initalize App  vars
mongo = PyMongo(app)

# Initalize modules/blueprints
from app.challenges.controller import module as challenge_module
app.register_blueprint(challenge_module)

from app.users.controller import module as users_module
app.register_blueprint(users_module)

from app.oauth.controller import module as oauth_module
app.register_blueprint(oauth_module, url_prefix='')

from app.realistic1.controller import module as real1_module
app.register_blueprint(real1_module)

from app.admin.controller import module as admin_module
app.register_blueprint(admin_module)


# Setup domain root routes
@app.route("/")
@app.route("/welcome/")
def home():
    return render_template('index.html')


# Route is used for certbot/Let's Encrypt to verify domain ownership
@app.route('/.well-known/acme-challenge/<token_value>')
def letsencrpyt(token_value):
    with open(app.config['BASE_DIR'] + '/.well-known/acme-challenge/{}'.format(token_value)) as f:
        answer = f.readline().strip()
    return answer


@app.route("/user-agent")
def intermediate3():
    import app.config.missions 
    if request.headers.get('User-Agent') == 'gotcharules':
        return 'The flag is: ' + app.config.missions.get_mission('intermediate3')['flag']
    return 'Your user-agent is not correct.'

@app.route("/basic/just/gonna/put/this/here/password.txt")
def basic2():
    import app.config.missions 
    return app.config.missions.get_mission('basic2')['flag']

@app.route("/robots.txt")
def basic3():
    import app.config.missions 
    return app.config.missions.get_mission('basic3')['flag']

@app.route('/dronepage/')
def realistic1():
    return redirect(url_for('realistic1.dronepage'))    


''' Handler that puts userinfo into every request/template '''
@app.before_request
def setup_userinfo():
    import user

    discord_info = user.get_discord()
    if not discord_info: g.userinfo = None
    else:
        ui = user.get_user_document(discord_info['id'])
        if not ui: g.userinfo = None
        else: g.userinfo = ui
    app.jinja_env.globals['userinfo'] = g.userinfo 
    app.jinja_env.globals['HOST'] = request.headers.get('Host', '')
    app.jinja_env.globals['NOW'] = datetime.datetime.now()


