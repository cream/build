import os
import sys
import json
import re
import shutil
import tempfile

import builder.helper
import builder.common

class BasePackage:

    def __init__(self, pkg_name, pkg_dest=None):

        pkg_info_path = os.path.join(builder.common.SRC_DIR, pkg_name, 'pkginfo')
        self.pkg_info = json.load(open(pkg_info_path))

        if pkg_dest:
            self.dst = os.path.join(pkg_dest, pkg_name)
        else:
            tmp = tempfile.mkdtemp(prefix='cream-builder-')
            self.dst = os.path.join(tmp, pkg_name)


    def prepare_build_tree(self):

        src = os.path.join(builder.common.SRC_DIR, self.pkg_name, builder.helper.guess_distribution())

        shutil.copytree(src, self.dst)
        os.chdir(self.dst)

        return self.dst


    def process_template(self, path):

        def replace(m):
            tag = m.group('tag').strip()
            return self.pkg_info[tag]

        fd = open(path, 'r')
        data = fd.read()
        fd.close()

        e = re.compile('{{(?P<tag>.*?)}}')

        data = e.sub(replace, data)

        fd = open(path, 'w')
        fd.write(data)
        fd.close()


    def build(self):
        pass
