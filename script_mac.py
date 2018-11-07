import subprocess
import re
str = subprocess.check_output(["wl","-a","eth1","assoclist"])
#str = "assoclist 8C:F5:A3:42:62:9B\nassoclist AC:5F:3E:B3:3C:8B\n"

matchList = re.findall(r"(?:[A-F0-9]{2}:){5}[A-F0-9]{2}",str,0)


if matchList :
	print("match")
else:
	print("no match")
	
print("\n")

print(matchList)


