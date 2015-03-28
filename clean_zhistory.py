#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# (
# export LC_ALL=C TMPID=`uuidgen`
# cat $HISTFILE | perl -pe s/'\\\n'/$TMPID/ | sort -t';' -k2 -u | sort -t';' -k1 | perl -pe s/$TMPID/'\\\n'/g
# )

import sys
import uuid
import difflib

sep = str(uuid.uuid4())


def print_help():
    print("usage: %s".format(sys.argv[0]))


def check_arg(argc):
    if argc >= 2:
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


def sort_lines(histfile):
    print(histfile.split('0;')[1])
    exit()


def main():
    argvs = sys.argv
    argc = len(argvs)
    if not check_arg(argc):
        print_help()
        return 0

    histpath = argvs[1]
    with open(histpath, encoding='utf-8') as histfile:
        # replace_newline
        command_dict = {}
        last_cmdline = []
        for histline in histfile:
            if histline.startswith(": 1"):
                last_cmdline = [histline.rstrip()]
                # print("last_cmdline: {} = {}".format(type(last_cmdline), last_cmdline))
            else:
                last_cmdline.append(histline.rstrip())
                # print("last_cmdline: {} = {}".format(type(last_cmdline), last_cmdline))
            timestamp, cmd0 = last_cmdline[0].split(';', 1)
            cmdlines = [cmd0]
            cmdlines.extend(last_cmdline[1:])
            command = sep.join(cmdlines)
            # print("command: {} = {}".format(type(command), command))
            command_dict[command] = timestamp
            #print("{};{}".format(command_dict[command], command))

        # sort_lines
        # clean_dupes
        last_command = ""
        for command, timestamp in sorted(command_dict.items()):
            # print("{};{}".format(timestamp, command))
            similarity = difflib.SequenceMatcher(None, last_command, command).ratio()
            if 0.8 < similarity:
                #print("{}\n{}\n{}\n".format(last_command, command, similarity))
                index = command.find(last_command)
                if index != -1:
                    #print(index)
                    #print("{}\n{}\n{}\n".format(last_command, command, similarity))
                    del command_dict[last_command]
            last_command = command

        # reformat
        import re

        histlines = []
        for command, timestamp in sorted(command_dict.items(), key=lambda x: x[1]):
            # print("{};{}".format(timestamp, command))
            cmdline = ["{};{}".format(timestamp, command)]
            #print(type(cmdline))
            for a_cmd in cmdline:
                multi_cmd_list = re.split(sep, a_cmd)
                #print(multi_cmd_list)
                histlines.extend(multi_cmd_list)

        # print_result
        for histline in histlines:
            print(histline)


# for script
if __name__ == '__main__':
    main()
