#!/usr/bin/env python

# Adding copyright line to all source files
#
# Use example: add_copyright.py <directory>

import glob
import sys
import os

# Variables
copyright_java_gradle_c_h = "// Copyright (C) Add-copyright-here"
copyright_pro_mk = "# Copyright (C) Add-copyright-here"
copyright_xml = '<?xml version="1.0" encoding="utf-8"?>\n<!-- Copyright (C) Add-copyright-here -->'

accepted_extensions = ["*.java", "*.xml", "build.gradle", "*.c", "*.h", "*.mk", "proguard-rules.pro"]
given_path = sys.argv[1]


def search_files(directory, extension):
    search_path = os.path.join(directory, "**", extension)
    found_paths = []
    for dir in glob.glob(search_path, recursive=True):
        found_paths.append(dir)
    return found_paths


def add_line(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n\n' + content)
    return True


if __name__ == '__main__':

    print("Checking if path is correct: ", given_path)
    if not os.path.isdir(given_path):
        raise Exception(f"ERROR! Given argument '{given_path}' is not a directory.")

    all_files = []
    for ext in accepted_extensions:
        all_files.extend(search_files(given_path, ext))

    print(all_files)

    for file in all_files:
        if file.endswith(('.java', 'build.gradle', '.c', '.h')):
            add_line(file, copyright_java_gradle_c_h)
        elif file.endswith(('proguard-rules.pro', '.mk')):
            add_line(file, copyright_pro_mk)
        elif file.endswith('.xml'):
            add_line(file, copyright_xml)

    print("\nDone!\n")


