#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# wsolver, a simple whitespace solver
# Copyright (C) 2019 Toni Helminen
#
# wsolver is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wsolver is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/>.
##

import os, time, sys, fnmatch

NAME    = "wsolver"
VERSION = "1.4"
AUTHOR  = "Toni Helminen"

###
## Modify starts
###

# Ignore these files | Depends from project to project
IGNORE_FILES  = ["[mM]akefile", "wsolver.py", "logo.jpg", "LICENSE"] # Unix style matching

# Convert tabs to how many spaces
TAB_TO_SPACES = "  "

# Directory to start
CURRENT_DIR   = "."

# Recursively go through all files and folders
RECURSIVE     = True # True | False

# Only cleanup this file
FILE          = False # ie. "wsolver.py"

# Convert tabs->spaces / remove whitespace / do both
MODE          = "both" # both / tabs / spaces

###
## Modify ends
###

def file_list_dir():
  return [os.path.join(CURRENT_DIR, f) for f in os.listdir(CURRENT_DIR) if os.path.isfile(os.path.join(CURRENT_DIR, f)) and not any(fnmatch.fnmatch(f, pattern) for pattern in IGNORE_FILES)]

def file_list_recursive():
  flist = []
  for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
      if any(fnmatch.fnmatch(name, pattern) for pattern in IGNORE_FILES):
        continue
      flist.append(os.path.join(root, name))
  return flist

def file_list():
  if FILE != False and os.path.isfile(os.path.join(CURRENT_DIR, FILE)):
    return [os.path.join(CURRENT_DIR, FILE)]
    
  return file_list_recursive() if RECURSIVE else file_list_dir()

def tabs2spaces(flist):
  tabs = 0
  for name in flist:
    f = open(name, 'r')
    s = f.read()
    for c in s:
      if c == '\t':
        tabs += 1
    s = s.replace("\t", TAB_TO_SPACES)
    f.close()
    f = open(name, 'w')
    f.write(s)
    f.close()
  return tabs

def cleanup_whitespace(flist):
  space_saved = 0
  for name in flist:
    k = os.path.getsize(name)
    f, lines = open(name, "r"), []
    for s in f.readlines():
      lines.append(s.rstrip())
    f.close()
    f = open(name, "w")
    f.write("\n".join(lines))
    f.close()
    space_saved += k - os.path.getsize(name)
  return space_saved

def work():
  flist, space_saved, tabs, mode = file_list(), 0, 0, 3
  if MODE == "tabs":
    mode = 1
  if MODE == "spaces":
    mode = 2
  if mode & 1:
    space_saved = cleanup_whitespace(flist)
  if mode & 2:
    tabs = tabs2spaces(flist)
  return {"tabs": tabs, "space_saved": space_saved, "files_touched": len(flist)}

def go():
  start = time.time()
  res = work()

  print("{ # Job done!")
  print("  time          = %.3fs," % (time.time() - start))
  print("  tabs          = %d," % (res["tabs"]))
  print("  space_saved   = %d," % (res["space_saved"]))
  print("  files_touched = %d" % (res["files_touched"]))
  print("}")

def main():
  print("{ # Version")
  print("  name        = %s," % (NAME))
  print("  version     = %s," % (VERSION))
  print("  author      = %s," % (AUTHOR))
  print("  description = Removes whitespace + tabs -> spaces")
  print("}\n")

  print ("{ # Working ...\n}\n")
  go()

if __name__ == "__main__":
  main()
