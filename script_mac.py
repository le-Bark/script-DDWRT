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
	matchList.sort()
	index1=0
	index2=0
	#si rien n'est vide
	if matchList2 and matchList:
		#verifie les changements
		while 1:
			if index1 == len(matchList) and index2 == len(matchList2):
				break
			elif index1 == len(matchList):
				evenements += [Evenement("depart",matchList2[index2])]
				index2+=1
			elif index2 == len(matchList2):
				evenements += [Evenement("ajout",matchList[index1])]
				index1+=1
			
			#nouveau resultat
			elif matchList[index1] < matchList2[index2]:
				evenements += [Evenement("ajout",matchList[index1])]
				index1+=1
				
			#depart
			elif matchList[index1] > matchList2[index2]:
				evenements += [Evenement("depart",matchList2[index2])]
				index2+=1
			#egal encore la
			elif matchList[index1] == matchList2[index2]:
				index1+=1
				index2+=1

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
