import os, sys
import re, subprocess
BASE_DIR = os.path.abspath(os.path.dirname(__file__)+'/../')
sys.path.insert(0, BASE_DIR)


# This script generates a roughly linear progress between
# Recruit (all noob challenges) and *** General. The *** rank
# is caluclates by taking MAX points and subtracting adv_min 
# missing_adv times. Meaing *** is ~MAX - missing_adv adv missions

noob_max = 51 # Max point value for noob challenges
adv_min = 300 # Min points for advanced challenges
missing_adv = 3

from app.config import ranks
ORIGINAL = ranks.get_ranks()
ranks = ORIGINAL.keys()


from app.config import missions
MISSIONS = missions.get_missions()
start = sum([int(MISSIONS[m]['exp']) for m in MISSIONS if int(MISSIONS[m]['exp']) < noob_max])
end = sum([int(MISSIONS[m]['exp']) for m in MISSIONS]) - (adv_min*3)


step = step = (end-start)/(len(ORIGINAL)-1)
new = []
new.append(start)

for i in range(len(ranks)-2):
	points = (i+1)*step + start
	if points % 100 > 50:
		points = int(round(points, -2))
	else:
		points = int(round(points, -2)) + 50
	new.append(points)
new.append(end)

for i,v in enumerate(new):
	ORIGINAL[ranks[i]]['points'] = v


for rank in ORIGINAL:
	print("[%s]" % rank)
	for key in ORIGINAL[rank]:
		print("%s:%s" % (key, ORIGINAL[rank][key]))
	print("")



