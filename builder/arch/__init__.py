import builder
import builder.helper
import builder.package
import builder.common

import subprocess
import os
import tempfile

class ArchPackage(builder.package.BasePackage):

    def __init__(self, pkg_name):

        self.pkg_name = pkg_name


    def build(self):

        os.chdir(os.path.join(builder.common.PKG_DIR, self.pkg_name, builder.helper.guess_distribution()))

        path = tempfile.mkdtemp(prefix='cream-builder-')

        pkgdest = os.path.join(path, 'pkg')
        srcdest = os.path.join(path, 'src')
        os.mkdir(pkgdest)
        os.mkdir(srcdest)

        p = subprocess.Popen(['makepkg', '-cf'], env={'PKGDEST': pkgdest, 'SRCDEST': srcdest})
        ret = os.waitpid(p.pid, 0)[1]

        if ret != 0:
            return False
        else:
            return pkgdest
