import builder
import builder.package
import builder.common

import os
import time
import urllib
import locale
import shutil
import tempfile
import subprocess


class DebianPackage(builder.package.BasePackage):

    def __init__(self, src, dest, jinja_env, options):

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        builder.package.BasePackage.__init__(self, src, dest, jinja_env, options)

        self.pkg_info['timestamp'] = time.strftime('%a, %d %b %Y %H:%M:%S +0100')

        self.pkg_name = '{0}-{1}-{2}'.format(self.pkg_info['name'],
                                        self.pkg_info['version'],
                                        self.pkg_info['release']
        )

        self.files = [
            'debian/control',
            'debian/rules',
            'debian/copyright',
            'debian/changelog'
        ]


    def prepare_build_tree(self):

        os.mkdir(self.dest)

        # download tarball
        tarball = self.pkg_info['source']
        tarball = tarball.replace('$pkgname-$pkgver-$pkgrel', self.pkg_name)
        target = os.path.join(self.dest, tarball.split('/')[-1])
        urllib.urlretrieve(tarball, target)

        # unpack archive
        p = subprocess.Popen(['tar', '-xf', target, '--directory', self.dest])
        ret = os.waitpid(p.pid, 0)[1]
        if ret != 0:
            raise Exception


        build_dir = os.path.join(self.dest, self.pkg_name)
        os.mkdir(os.path.join(build_dir, 'debian'))
        for file_ in self.files:
            shutil.copy(os.path.join(self.src, file_), os.path.join(build_dir, file_))

        return build_dir


    def build(self):

        build_dir = self.prepare_build_tree()

        os.chdir(self.dest)
        for file_ in self.files:
            path = os.path.join(self.pkg_name, file_)
            self.process_template(path)

        os.chdir(build_dir)
        p = subprocess.Popen(['debuild', '--no-tgz-check'])
        ret = os.waitpid(p.pid, 0)[1]

        for i in os.listdir(self.dest):
            if i.endswith('.deb'):
                package_path = os.path.join(self.dest, i)

        if ret != 0:
            return False
        else:
            return package_path
