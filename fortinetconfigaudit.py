import socket
import re
import paramiko
with open('hosts.all.txt') as f:
    for line in f:
        line = line.strip()
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if len(re.findall('[A-Za-z]',line)) > 0:
            try:
		hostname = line
                line = socket.gethostbyname(line)
            except:
                print "Error polling DNS for %s" % (line)
        else:
            line = line
        try:
            dssh.connect(line, username='username', password='password')
        except paramiko.ssh_exception.AuthenticationException:
            print "Authentication error recived when connecting to %s" % (line)
            continue
        except:
            print "Error connecting to %s :: socket error" % (line)
            continue
        print 'running script on store: %s' % (line)
        try:
          stdin, stdout, stderr = dssh.exec_command('get firewall address')
        except:
          print "error sending command to device"
          continue
        mystring = stdout.read()
        x = mystring.split('\n')
	contents=[]
        for i in x:
            a = re.findall('vxn1.datawire.net-205.167.140.10',i)
	    if len(a) > 0:
		contents.append(i)
	if len(contents) == 0:
                log = open('output-configaudit.txt', 'a+')
                log.write(hostname+'\n')
                log.write(i+'\n')
                log.close()
    dssh.close()
