import os, sys
import re, subprocess
BASE_DIR = os.path.abspath(os.path.dirname(__file__)+'/../')
sys.path.insert(0, BASE_DIR)

# This script is intended to be used after a significant rank or mission
# changes. It will loop over all entries in the db and re-calculate their
# rank and adjust their rank on discord.


# I wrote this class for another project, eventually it'll get merged into the 
# discord file but for now I'll just use it here
import httplib2, cgi, json, logging, copy, time
class JsonClient(object):
    _retry_rate = 60
    _headers = {}
    _http = None
    _log = None

    def __init__(self, headers=None, retry_rate=60, http=None):
        self._retry_rate = retry_rate
        self._log = logging.getLogger(self.__class__.__name__)
        if headers != None:
            self._headers = headers
        
        self._http = http
        if self._http == None:
            self._http = httplib2.Http()

    def req(self, method, url, headers=None, body=None):
        self._log.debug("[%s] %s", method, url)

        tmp_headers = copy.deepcopy(self._headers)
        if headers != None:
            tmp_headers.update(headers)


        while True:
            res, content = self._http.request(url, method=method, body=body, headers=tmp_headers)
            _, content_type_params = cgi.parse_header(res.get('content-type', 'application/json; charset=UTF-8'))
            charset = content_type_params.get('charset', 'UTF-8')
            content = content.decode(charset)

            self._log.debug('Got HTTP %s', res['status'])
            status_code = int(res['status'])
            if status_code > 299:
                self._log.error("Unexpected response code: %s", res['status'])

            if int(res['status']) >= 500:
                self_log.error("Encountered a server error, retrying in %d seconds", self.retry_rate)
                time.sleep(self._retry_rate)
            else:
                #Break the loop if we are not retrying
                break

        try:
            j = json.loads(content)
            return res, j
        except:
            #self._log.error("Failed to parse response.")
            return res, None

    def get(self,url,headers=None):
        return self.req('GET', url, headers)

    def post(self, url, content_type='application/x-www-form-urlencoded', headers=None, body=None):
        if headers == None: headers = {}
        headers['content-type'] = content_type
        return self.req("POST", url, headers=headers, body=body)

    '''Updates the value of a header for a client'''
    def set_header(self, header_name, value):
        self._log.debug("Set Header: %s => '%s'", header_name,value)
        self._headers[header_name] = value

    '''Removes a header for a client'''
    def delete_header(self, header_name):
        self._log.debug("Removing header: %s", name, header_name)
        del self._headers[header_name]

import logging, json, time
class DiscordClient(object):
    _client  = None
    _headers = {}
    _auth_token = None
    _log = None
    _base_url = 'https://discordapp.com/api'
    _last_res = {
        "x-ratelimit-remaining": "10",
        "x-ratelimit-limit": "10",
        "x-ratelimit-reset": "0",
    }


    def __init__(self,auth_token):
        self._auth_token = auth_token
        self._headers = {
            'user-agent': 'NetcatAPI (netcat.us, 0.01)',
            'Authorization':'Bot '+ self._auth_token
        }
        self._client = JsonClient(headers=self._headers)
        self._log = logging.getLogger(self.__class__.__name__)

    def check_limits(self,block=True):
        now = int(time.time())
        reset = int(self._last_res.get('x-ratelimit-reset', "0"))
        if self._last_res.get('x-ratelimit-remaining', "9") == "0":
            now = int(time.time())
            reset = int(self._last_res.get('x-ratelimit-reset', "0"))
            delta = reset - now
            if delta > 0 and block:
                self._log.warning("Hit discord-api rate limit, sleeping for %f seconds.", delta)
                time.sleep(delta)
            elif delta > 0:
                return delta
        return 0

    def _get(self,path):
        self.check_limits()
        res, j = self._client.get(self._base_url + path)
        self._last_res = res
        return j

    def _delete(self, path):
        self.check_limits()
        res,j = self._client.req('DELETE', self._base_url + path)
        self._last_res = res
        return j

    def _put(self, path, data=None):
        self.check_limits()
        res,j = self._client.req('PUT', self._base_url + path, headers={'content-type':'application/json'}, body=data)
        self._last_res = res
        return j

    def _patch(self, path, data=None):
        self.check_limits()
        res,j = self._client.req('PATCH', self._base_url + path, headers={'content-type':'application/json'},body=data)
        self._last_res = res
        return j

    def _guild_members_req(self,gid,limit=1000, after=None):
        path = '/guilds/{}/members?limit={}'.format(gid, limit)
        if after:
            path += '&after=' + after
        return self._get(path)

    def guild_members(self, gid):
        gm = self._guild_members_req(gid, 1000)
        last = gm
        while len(last) == 1000:
            last = self._guild_members_req(gid, 1000, last[-1]['user']['id'])
            gm.extend(last)
        self._log.debug('Got %d members.', len(gm))
        return gm


import app
import sys
import app.config.ranks as ranks
logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)
LOG = logging.getLogger('RerankScript')
with app.app.app_context():
    discord = DiscordClient(app.app.config['BOT_TOKEN'])
    gm = discord.guild_members(app.app.config['GUILD_ID'])
    all_ranks = ranks.get_ranks()

    members = {}
    for m in gm: members[m['user']['id']] = m

    #cur = app.mongo.db.users.find({"exp":{"$gt":0}})
    cur = app.mongo.db.users.find({})
    for userinfo in cur:
        needs_update = False
        if not 'rank' in userinfo: 
            #Apaprently some acocunts don't even have a rank so give an empty one for now
            app.mongo.db.users.update_one({"_id" : userinfo['_id'] }, {'$set' : {"rank":""}})
            userinfo['rank'] = ''


        points = app.user.calculate_points(userinfo)
        if points != userinfo['exp']:
            needs_update = True
        
        new_rank = ranks.lookup_rank(points)
        #If they havn't earned a rank translate the None response to a dict with the needed info
        if new_rank == None: new_rank = {'name':''}
        if new_rank['name'] != userinfo['rank']: needs_update = True

        if needs_update:
            LOG.info("Database: %s Old:%s(%d) New:%s(%d)", userinfo['name'].encode('punycode'), userinfo['rank'], userinfo['exp'], new_rank['name'], points)
            app.mongo.db.users.update_one({"_id" : userinfo['_id'] }, {'$set' : {"exp":points, "rank":new_rank['name']}})


        #Update Discord if the user is in discord
        if userinfo['id'] in members:
            passed = False
            set_ranks = []
            unset_ranks = []
            new_rank = new_rank['name']
            if new_rank == '': passed = True
            
            # Loop over the ranks and split set/unset appropiately
            for r in all_ranks.keys():
                if passed: unset_ranks.append(app.discord.ROLES[all_ranks[r]['role']])
                else: set_ranks.append(app.discord.ROLES[all_ranks[r]['role']])
                if all_ranks[r]['name'] == new_rank: passed = True

            #Put all the non-rank roles into the set_ranks list
            for r in members[userinfo['id']]['roles']:
                if not r in unset_ranks and not r in set_ranks:
                    set_ranks.append(r)


            #Check if we needs to update thier ranks of not
            if len(set_ranks) != len(members[userinfo['id']]['roles']):
                LOG.info("Discord: %s - %s", userinfo['name'].encode('punycode'), new_rank)
                #Generate the JSON
                patch_data = ''
                for r in set_ranks:
                    patch_data += '"{}",'.format(r)
                patch_data = '{"roles":[%s]}'%(patch_data[:-1])
                discord._patch('/guilds/{}/members/{}'.format(app.app.config['GUILD_ID'], userinfo['id']), patch_data)
            del members[userinfo['id']]
    

    rank_roles = [app.discord.ROLES[all_ranks[rank]['role']] for rank in all_ranks]
    for mem in members:
        cur = members[mem]
        new_roles = [role for role in cur['roles'] if not role in rank_roles]
        if len(new_roles) != len(cur['roles']):
            LOG.info("Discord: %s - Not on netcat but has rank related roles.", cur['user']['username'].encode('punycode'))
            patch_data = ''
            for r in new_roles:
                patch_data += '"{}",'.format(r)
            patch_data = '{"roles":[%s]}'%(patch_data[:-1])
            discord._patch('/guilds/{}/members/{}'.format(app.app.config['GUILD_ID'], cur['user']['id']), patch_data)

    
