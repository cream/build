import os
import json
import shutil

import builder.helper
import builder.common

class BasePackage(object):

    def __init__(self, src, dest, jinja_env, options):

        self.src = src
        self.dest = dest
        self.jinja_env = jinja_env
        self.options = options

        pkg_info_path = os.path.join(src, 'pkginfo')
        self.pkg_info = json.load(open(pkg_info_path))


    def prepare_build_tree(self):

        src = os.path.join(self.src, builder.helper.guess_distribution())

        shutil.copytree(src, self.dest)
        os.chdir(self.dest)

        return self.dest


    def process_template(self, name):
        template = self.jinja_env.get_template(name)

        with open(name, 'w') as file_handle:
            file_handle.write(template.render(self.pkg_info))


    def build(self):
        pass
