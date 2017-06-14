#!/usr/bin/env python

import os
import sys
import re

title_regex = re.compile(r'tvg-name="(.+)" t')

def main(fileName):
    fp = open(fileName)
    prev = ""
    count = 0
    films = []
    for line in fp.readlines():
        if line.startswith('#'):
            prev = line
        else:
            if line.startswith("http"):
                title = title_regex.findall(prev)[0].replace(' ','_').replace('-[','').replace(']-','')
                
                if title.startswith('_') or title.endswith('_'):
                    title = title[1:-1]
                films.append({
                    "title" : title,
                    "url" : line.replace('\r\n','')
                })

        count += 1

    fp.close()

    return { 
            "count" : count,
            "films" : films
    }


def getWgetCmd(dictionary):
    cmds = []
    for item in dictionary['films']:
        ext = item['url'].split('.')[-1]
        cmds.append("wget %s -O %s.%s" % ( item['url'], item['title'], ext ))

    return cmds

if __name__ == "__main__":
    if len(sys.argv) > 1:
        res = main(sys.argv[1])
        l = getWgetCmd(res)
        print "\n".join(l)
