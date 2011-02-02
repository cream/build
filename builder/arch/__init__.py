import builder
import builder.package
import builder.common

import subprocess
import os

class ArchPackage(builder.package.BasePackage):

    def __init__(self, src, dest, jinja_env):
        builder.package.BasePackage.__init__(self, src, dest, jinja_env)


    def build(self):

        build_dir = self.prepare_build_tree()
        self.process_template('PKGBUILD')

        p = subprocess.Popen(['makepkg', '-cf'])
        ret = os.waitpid(p.pid, 0)[1]

        for i in os.listdir(build_dir):
            if i.endswith('.pkg.tar.xz'):
                package_path = os.path.join(build_dir, i)

        if ret != 0:
            return False
        else:
            return package_path
