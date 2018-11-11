import subprocess
import re
import time
import datetime
import firebase_admin
from pathlib import Path

from firebase_admin import credentials
from firebase_admin import db


class Evenement:
	def __init__(self,type,adresse):
		self.type = type
		self.adresse = adresse
	type = "type"
	adresse = "00:00:00:00:00:00"

#recuperation du path vers le volume "logs"
pathStr = subprocess.check_output(["lsblk","-o","label,mountpoint"]).decode("UTF-8")
#extraction du path depuis le resusltat
pathStr = re.findall(r"LOGS\s+(.+)\s",pathStr)[0]

#lis l'identifiant du routeur dans le fichier de configuration sur la memoire externe

fichierConfig = open(pathStr + "/config.txt","r")
routeurId = fichierConfig.readline()
dbURL = fichierConfig.readline()
fichierConfig.close()

routeurId = re.findall(r"\w+",routeurId)[0]


#initialisation de al base de donee
cred = credentials.Certificate(pathStr + "/routeurKey.json")
firebase_admin.initialize_app(cred,{ "databaseURL" : dbURL})
dbRef = db.reference()

matchList2 = list()
matchList = list()
evenements = list()

macCheck = re.compile(r"(?:[A-F0-9]{2}:){5}[A-F0-9]{2}")

while 1:
	str = subprocess.check_output(["wl","-a","eth1","assoclist"])
	matchList = macCheck.findall(str.decode("UTF-8"),0)
	
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
		dbRef.child(routeurId).push({
			"type" : x.type,
			"adresse" : x.adresse,
			"heure" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		})

	evenements = []
