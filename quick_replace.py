#!/.autodirect/app/Python-2.release/bin/python
# -*- coding: utf-8 -*-
"""
Owner               : Oron Golan <oronboni@hotmail.com>

Created on          : Dec 17, 2016

Description         :  Read Jenkins job parameters
                        for https://python-jenkins.readthedocs.org/


"""

#############################
# Python built-in imports
#############################
import argparse
import subprocess
import os

def print_options(options):
    print "Build number: %s" % options.build_number
    print "Pom.xml location: %s" % options.pom_path


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--build_number", help="Build number", default="1")
    parser.add_argument("-p", "--pom_path", help="Command status", default="start")
    options = parser.parse_args()
    print_options(options)
    return vars(options)


def replace(build_number, pom_path):
    # Read in the file
    filedata = None
    with open(pom_path, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('<version>0.0.1-SNAPSHOT</version>', '<version>0.0.1.' + build_number + '</version>')
    filedata = filedata.replace('${mtd.version}', '0.0.1.' + build_number + '')

    # Write the file out again
    with open(pom_path, 'w') as file:
        file.write(filedata)


def main():
    print '**** Read jobs parameters start'
    options = get_args()
    build_number = options["build_number"]
    pom_path = options["pom_path"]

    replace(build_number, pom_path)

    dir_path = os.path.dirname(os.path.realpath(pom_path))

    dirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    for dir_name in dirs:
        if os.path.isfile(dir_path +'/' + dir_name + '/pom.xml'):
            replace (build_number, dir_path +'/' + dir_name + '/pom.xml')

if __name__ == "__main__":
    main()

