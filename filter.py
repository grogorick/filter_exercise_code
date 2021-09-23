#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil

supported = [
  { "ext": [".txt", ".py"],         "replacement": "{}#\n{}# ???\n{}#\n" },
  { "ext": [".cpp", ".h", ".inl"],  "replacement": "{}/*\n{} ???\n {}*/\n" }
  ]

exclude_dirs_that_start_with = (".", "_", "cmake-", "build-", "logs_")
exclude_files_that_start_with = (".", "_")

additional_exclude_dirs_filename = "_filter_exclude_dirs"
additional_exclude_files_filename = "_filter_exclude_files"

def filter_file(filename, lines, solution, comments):

    filtered_content = []

    ignore = False
    indent =  ""
    for l in lines:

        if "@EXERCISE" in l: # start solution code
            if "==>" in l:
                ignore = False
            else:
                ignore = not solution
            indent = l[:len(l) - len(l.lstrip())]
            continue

        if "==>" in l: # start exercise code
            ignore = solution
            continue

        if "== ==" in l: # start test code (neither in task nor in solution code)
            ignore = True
            continue

        if "<==" in l: # end code, place ??? here
            if not solution:
                filtered_content.append(comments["replacement"].format(*([indent] * 3)))
            ignore = False
            continue

        if "===" in l: # end code without ???
            ignore = False
            continue

        if ignore:
            continue

        filtered_content.append(l)
    return filtered_content

if len(sys.argv) <= 2:
  print("> " + sys.argv[0] + " <task-dir> <exercise|solution>")
  exit()

solution = sys.argv[2] == "solution"

base_dir = sys.argv[1]
if base_dir[-1] not in ["/", "\\"]:
  base_dir = base_dir + "/"
dirname = base_dir[:-2] # sheetXX_/ -> sheetXX

base_outDir = dirname + ("_solution" if solution else "") + "/"

def filter_directory(path, exclude_dirs, exclude_files):
  dir = base_dir + path
  outDir = base_outDir + path
  if not os.path.exists(outDir):
    os.makedirs(outDir)

  if os.path.isfile(dir + additional_exclude_dirs_filename):
    with open(dir + additional_exclude_dirs_filename) as f:
      exclude_dirs += tuple(filter(None, f.read().splitlines()))

  if os.path.isfile(dir + additional_exclude_files_filename):
    with open(dir + additional_exclude_files_filename) as f:
      exclude_files += tuple(filter(None, f.read().splitlines()))

  _, directories, filenames = next(os.walk(dir), (None, [], []))
  for filename in filenames:
    if filename.startswith(exclude_files):
      continue

    print("\n" + dir + filename + " ------------------------------")

    file_ext = filename.rfind('.')
    file_ext = filename[file_ext:] if file_ext > -1 else None

    comments = {}
    for s in supported:
        if file_ext in s["ext"]:
            comments["replacement"] = s["replacement"]

    if not any([file_ext in s["ext"] for s in supported]):
      print("- File extension " + file_ext + " not supported. File will be copied as is.\n")
      shutil.copy2(dir + filename, outDir)
      continue

    print("- Filter file...\n")
    lines = []
    with open(dir + filename, "r") as f:
      lines = f.readlines()
    lines = filter_file(filename, lines, solution, comments)
    for line in lines:
      print(line, end="")
    with open(outDir + filename, "w") as f:
      f.writelines("".join(lines))

  for subdir in [p for p in directories if len(p) > 0 and not p.startswith(exclude_dirs)]:
    filter_directory(path + subdir + "/", exclude_dirs, exclude_files)

filter_directory("", exclude_dirs_that_start_with, exclude_files_that_start_with)