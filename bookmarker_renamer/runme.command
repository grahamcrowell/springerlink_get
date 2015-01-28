#!/bin/bash
cwd="$( dirname "$0" )"
cd $cwd
echo ls
python springer_bookmarks.py
