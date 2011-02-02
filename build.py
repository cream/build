#! /usr/bin/env python
# -*- coding: utf-8 -*-

import builder
from builder import helper
from builder import arch
from builder import debian

from builder.common import SRC_DIR

import os
import optparse
import tempfile

from jinja2 import Environment, FileSystemLoader

PACKAGES = {
    'arch': arch.ArchPackage,
    'debian': debian.DebianPackage
}

class Builder(object):

    def __init__(self, package_name):

        self.package_name = package_name

        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.template_path = os.path.join(self.base_path, 'builder', 'templates')
        self.package_dest = tempfile.mkdtemp(prefix='cream-builder-')

        self.distribution = helper.guess_distribution()


    def build_package(self, package, name):

        print " » Building '{0}' for {1}".format(name, self.distribution)

        print "\n" + 40*' -' + '\n'
        status = package.build()
        print '\n' + 40*' -' + '\n'

        if status:
            print " » The build process was successful!"
            print "   → You may find the package in '{0}'…".format(status)
        else:
            print " » Build process failed!"


    def build(self):

        if self.package_name == 'all':
            for pkg in os.listdir(SRC_DIR):
                pkg_src = os.path.join(SRC_DIR, pkg)
                pkg_dest = os.path.join(self.package_dest, pkg)

                jinja_env = Environment(loader=FileSystemLoader([self.template_path, pkg_dest]))

                package = PACKAGES[self.distribution]
                p = package(pkg_src, pkg_dest, jinja_env)

                self.build_package(p, pkg)

                os.chdir(self.base_path)
        else:
            pkg_src = os.path.join(SRC_DIR, self.package_name)
            pkg_dest = os.path.join(self.package_dest, self.package_name)

            jinja_env = Environment(loader=FileSystemLoader([self.template_path, pkg_dest]))

            package = PACKAGES[self.distribution]
            p = package(pkg_src, pkg_dest, jinja_env)

            self.build_package(p, self.package_name)





if __name__ == '__main__':
    parser = optparse.OptionParser()
    options, args = parser.parse_args()
    package_name = args[0]

    builder = Builder(package_name)
    builder.build()

    print " » Done building packages"
