import socket
import re
import paramiko
with open('hosts') as f:
    for line in f:
        line = line.strip()
        dssh = paramiko.SSHClient()
        dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if len(re.findall('[A-Za-z]',line)) > 0:
            try:
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
          stdin, stdout, stderr = dssh.exec_command('diagnose hardware deviceinfo disk')
        except:
          print "error sending command to device"
          continue
        mystring = stdout.read()
        x = mystring.split('\n')
        print x
        for i in x:
            a = re.findall('cannot get scsi device info',i)
            if len(a) > 0:
                log = open('output.txt', 'a+')
                log.write(line+'\n')
                log.write(i+'\n')
                log.close()
    dssh.close()
