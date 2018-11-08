import subprocess
import re
import time

class Evenement:
	def __init__(self,type,adresse):
		self.type = type
		self.adresse = adresse
	type = "type"
	adresse = "00:00:00:00:00:00"

matchList2 = list()
matchList = list()
evenements = list()

while 1:
	str = subprocess.check_output(["wl","-a","eth1","assoclist"])
	matchList = re.findall(r"(?:[A-F0-9]{2}:){5}[A-F0-9]{2}",str.decode("UTF-8"),0)
	
	#si rien n'est vide
	if matchList2 and matchList:
		#nouvelles adresses present dans matchlist mais pas dans matchlist2
		for x in matchList:
			if x not in matchList2:
				evenements += [Evenement("ajout",x)]
		#depart adresses non present dans matchlist
		for x in matchList2:
			if x not in matchList:
				evenements += [Evenement("depart",x)]
	elif matchList:
		for x in matchList:
			evenements += [Evenement("ajout",x)]
	elif matchList2:
		for x in matchList2:
			evenements += [Evenement("depart",x)]
				
	matchList2 = matchList
	time.sleep(1)
				
	for x in evenements:
		print(f"{x.type} {x.adresse}")
	evenements = []
