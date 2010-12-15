import os
import re

def guess_distribution():

    if os.path.isfile('/etc/lsb-release'):
        return open('/etc/lsb-release').read()
    else:
        for i in os.listdir('/etc'):
            m = re.compile('(?P<dist>.*)\-release').match(i)
            if m:
                return m.group('dist')
