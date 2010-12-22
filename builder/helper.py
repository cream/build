import os
import re

def guess_distribution():

    if os.path.isfile('/etc/lsb-release'):
        with open('/etc/lsb-release') as fd:
            release = fd.read()
            dist = re.findall('DISTRIB_ID=(?P<dist>.*)', release)[0].lower()
            if dist in ['ubuntu', 'debian']:
                return 'debian'
            return dist
    else:
        for i in os.listdir('/etc'):
            m = re.compile('(?P<dist>.*)\-release').match(i)
            if m:
                return m.group('dist')
