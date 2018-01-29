import os, sys
import re, subprocess
BASE_DIR = os.path.abspath(os.path.dirname(__file__)+'/../')
sys.path.insert(0, BASE_DIR)

def check_state(tag):
    cmd = "docker ps -q --filter status=running --filter ancestor=%s | wc -l" % (tag)
    try:
        output = subprocess.check_output(cmd, shell=True)
        return int(output.strip())
    except subprocess.CalledProcessError as e:
        return 0;

def start(container):
    start_cmd = ''
    tag = container['tag']

    if container['ports'] and ':' in container['ports']:
        ports = container['ports'].split(':')
        start_cmd = "docker run -d -p {}:{} {}:latest".format(ports[1],ports[0], tag)
    else:
        start_cmd = "docker run -d {}".format(tag)

    try:
        o = subprocess.check_output(start_cmd, shell=True)
        print "Started: {}".format(tag)
    except subprocess.CalledProcessError as e:
        print "X"*60
        print "Failed to start {}\n{}".format(tag,e.output)
        print "X"*60


from app.config import missions
MISSIONS = missions.get_missions()

containers = {}
for mission in MISSIONS:
    m = MISSIONS[mission]
    if 'docker' in m:
        containers[m['name']] = {
            "tag":re.sub('[^0-9a-zA-Z]+', '',m['name']),
            "docker":m['docker'],
            "ports":m.get("ports", None),
        }

for c in containers:
    if not check_state(containers[c]['tag']):
        start(containers[c])