import subprocess


site_url = 'http://www.rolfny.com'
get_osInfo = subprocess.Popen(["python3.5","/var/www/py/armoredware.com/infosec/blackops/wig.py","-u",site_url,"&"],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
osInfo = get_osInfo.communicate()[0]
p_status = get_osInfo.wait()
print( osInfo)
