import json
import re
import string


def readRuntimeLogs(path: string):
    with open(path, encoding='utf-8') as file:
        count = 0;
        re_pattern = re.compile('([0-9]{2}[.][0-9]{2}[.][0-9]{4}\s[0-9]{2}[:][0-9]{2}[:][0-9]{2})')
        runtimeLog_list = {}
        for line in file:
            if re.findall(re_pattern, line):

                # _, data, value = re.split(re_pattern, line)
                _, data, value = re.split(re_pattern, line)
                value = value.replace(value[0], "", 1)
                runtimeLog_list[count] = (data, value)
                lastKey = count
                count = count + 1

            else:
                # str = f"{runtimeLog_list[lastKey][1]} {line}".rstrip().replace(" \t", "").replace(" \t\t", "")
                strn = f"{runtimeLog_list[lastKey][1]} {line} \t\n"
                runtimeLog_list[lastKey] = (data, strn)

    return runtimeLog_list


def readStartLogs(path: string):
    with open(path, encoding='utf-8') as file:
        count = 0;
        re_pattern = re.compile('([0-9]{2}[-][0-9]{2}[-][0-9]{4}\s[0-9]{2}[:][0-9]{2}[:][0-9]{2})')
        startLog_list = {}
        for line in file:
            if line != '\n':
                msgType, data, value = re.split(re_pattern, line)
                startLog_list[count] = (msgType, data, value)
                count = count + 1
            continue
    return startLog_list

