#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# (
# export LC_ALL=C TMPID=`uuidgen`
#   cat $HISTFILE | perl -pe s/'\\\n'/$TMPID/ | sort -t';' -k2 -u | sort -t';' -k1 | perl -pe s/$TMPID/'\\\n'/g
# )

import sys
import os
import uuid


sep = uuid.uuid4().__str__()


def print_help():
    print("usage: %s".format(sys.argv[0]))


def check_arg(argc):
    if argc == 2:
        return True
    else:
        return False


def read_histfile(histpath):
    with open(histpath, encoding='utf-8') as histfile:
        return histfile


def replace_newline(histfile):
    lines = histfile.read()
    return lines.replace('\\\n', sep)
    # line_number = 0
    # for line in histfile:
    #     #line_number += 1
    #     #print('{:>4} {}'.format(line_number, line.rstrip()))
    #     pass


def main():
    argvs = sys.argv
    argc = len(argvs)
    if not check_arg(argc):
        print_help()
        return 0

    histpath = argvs[1]
    with open(histpath, encoding='utf-8') as histfile:
        histfile = replace_newline(histfile)
        exit()
        sort_lines(histfile)
        clean_dups(histfile)
        reformat(histfile)
        print_result(histfile)

# for script
if __name__ == '__main__':
    main()
