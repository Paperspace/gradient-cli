import os
import subprocess
import sys
args = sys.argv[:]
print('hello from %s' % args[0])
print('args: ' + ' '.join(args))
print('current directory: ' + os.getcwd())
p = subprocess.Popen('ls -al', shell=True, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while True:
  line = p.stdout.readline()
  if line != '':
    print(line.rstrip())
  else:
    break
retval = p.wait()
print('%s done' % args[0])
