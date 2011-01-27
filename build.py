#! /usr/bin/env python
# -*- coding: utf-8 -*-

import builder
from builder import helper
from builder import arch
from builder import debian

import optparse

BUILDERS = {
    'arch': arch.ArchPackage,
    'debian': debian.DebianPackage
}

class Builder:

    def __init__(self):

        parser = optparse.OptionParser()
        (self.options, self.args) = parser.parse_args()

        pkg = self.args[0]

        print " » Building '{0}'…".format(pkg)
        print " » Guessing your distribution…"
        dist = helper.guess_distribution()

        print "   → {0}".format(dist)

        builder = BUILDERS[dist]
        p = builder(pkg)

        print " » Building package for '{0}'…".format(dist)

        print "\n" + 40*' -' + '\n'
        status = p.build()
        print '\n' + 40*' -' + '\n'

        if status:
            print " » The build process was successful!"
            print "   → You may find the package in '{0}'…".format(status)
        else:
            print " » Build process failed!"





if __name__ == '__main__':
    b = Builder()
