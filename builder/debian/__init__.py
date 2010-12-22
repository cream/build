import builder
import builder.package
import builder.common

import os
import time
import urllib
import shutil
import tempfile
import subprocess

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class DebianPackage(builder.package.BasePackage):

    def __init__(self, pkg_name):

        builder.package.BasePackage.__init__(self, pkg_name)

        self.pkg_info['timestamp'] = time.strftime('%a, %d %b %Y %H:%M:%S +0100')
        self.pkg_name = pkg_name

        self.files = [
            'changelog',
            'control',
            'copyright',
            'rules'
        ]

    def prepare_build_tree(self):

        pkg_name = '{0}-{1}-{2}'.format(self.pkg_info['name'],
                                        self.pkg_info['version'],
                                        self.pkg_info['release']
        )

        src = os.path.join(builder.common.SRC_DIR, self.pkg_name, builder.helper.guess_distribution())
        tmp = tempfile.mkdtemp(prefix='cream-builder-')
        package_dir = os.path.join(tmp, self.pkg_name)
        build_dir = os.path.join(tmp, self.pkg_name, pkg_name)

        os.mkdir(package_dir)

        # download tarball
        tarball = self.pkg_info['source']
        tarball = tarball.replace('$pkgname-$pkgver-$pkgrel', pkg_name)
        target = os.path.join(package_dir, tarball.split('/')[-1])
        urllib.urlretrieve(tarball, target)

        # unpack archive
        p = subprocess.Popen(['tar', '-xf', target, '--directory', package_dir])
        ret = os.waitpid(p.pid, 0)[1]
        if ret != 0:
            raise Exception

        os.mkdir(os.path.join(build_dir, 'debian'))
        for file_ in self.files:
            shutil.copy(os.path.join(src, file_), os.path.join(build_dir, 'debian', file_))
        os.chdir(build_dir)

        return package_dir, build_dir


    def build(self):

        package_dir, build_dir = self.prepare_build_tree()

        for file_ in self.files:
            path = os.path.join(build_dir, 'debian', file_)
            self.process_template(path)

        p = subprocess.Popen(['debuild', '--no-tgz-check'])
        ret = os.waitpid(p.pid, 0)[1]

        for i in os.listdir(package_dir):
            if i.endswith('.deb'):
                package_path = os.path.join(build_dir, i)

        if ret != 0:
            return False
        else:
            return package_path
