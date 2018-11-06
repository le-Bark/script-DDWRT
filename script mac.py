import subprocess

str = subprocess.check_output(["wl","-a","eth1","assoclist"])

print str
