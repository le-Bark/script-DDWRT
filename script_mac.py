import subprocess
import re
import time

class Evenement:
	def __init__(self,type,adresse):
		self.type = type
		self.adresse = adresse
	type = "type"
	adresse = "00:00:00:00:00:00"

#str = subprocess.check_output(["wl","-a","eth1","assoclist"])
str = "assoclist 8C:F5:A3:42:62:9B\nassoclist AC:5F:3E:B3:3C:8B\n"
resultList = [  "1,2,3,5",
				"1,2,3,5",
				"1,2,3,5",
				"1,2,3,5,6",
				",,,5,6",
				"1,2,3,5,6",
				"laksdj",
				"2",
				"",
				"",
				"",
				"",
				"1"]



matchList2 = list()
matchList = list()
evenements = list()


i=0
while i<len(resultList):
	#str = resultList[i]
	str = subprocess.check_output(["wl","-a","eth1","assoclist"])
	matchList = re.findall(r"(?:[A-F0-9]{2}:){5}[A-F0-9]{2}",str.decode("UTF-8",0)
	#matchList = re.findall(r"[1-9]{1,2}",str,0)
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
		for x in range(0,len(matchList)):
			evenements += [Evenement("ajout",matchList[x])]
	elif matchList2:
		for x in range(0,len(matchList2)):
			evenements += [Evenement("depart",matchList2[x])]
				
	matchList2 = matchList
	i+=1
	time.sleep(1)
				
	for x in range(0,len(evenements)):
		print(evenements[x].type + "  " + evenements[x].adresse)
	evenements = []
