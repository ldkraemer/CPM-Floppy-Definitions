#!/usr/bin/python3

import sys
import re

mode = 'SCAN'

try:
    infile = sys.argv[1]
except IndexError:
    usage = f"""Usage: {sys.argv[0]} filename

Splits a combined set of definitions into separate files
grouped by their intended application.
"""
    raise SystemExit(usage)

diskdef = infile + '.dd'
ff = infile + '.ff'
libdisk = infile + '.ldisk'
twotwodisk = infile + '.22'

cmtrx = re.compile('^\/\* Not in 22DISK')
ddrx = re.compile('^#\s+([0-9A-Z]{1,5})\s+', re.I)
ddendrx = re.compile('^end\s*')
ldrx = re.compile('^#\s*libdsk\s*$')
ffrx = re.compile('^#\s*flashfloppy')
sysrx = re.compile('^SYSTEM\s+(.*)$')
twotworx = re.compile('^BEGIN\s+(\S+)')

linenum = 0
try:
    with open(infile, "r") as infh, open(diskdef, "w") as d, open(ff, "w") as f, open(libdisk, "w") as l, open(twotwodisk, "w") as two:
        for line in infh:
            linenum += 1

            if re.match(cmtrx, line):
                continue
            
            twotwo_m = re.match(twotworx, line)
            dd_m = re.match(ddrx, line)
            ld_m = re.match(ldrx, line)
            ff_m = re.match(ffrx, line)
            sys_m = re.match(sysrx, line)
            
            if twotwo_m:
                mode = '22DISK'
                curdef = twotwo_m.group(1)
            elif dd_m:
                mode = 'DISKDEF'
                curdef = dd_m.group(1)
            elif ld_m:
                mode = 'LIBDISK'
                continue
            elif ff_m:
                mode = 'FF'
                f.write('# ' + curdef + '\n')
                continue
            elif sys_m:
                mode = 'SYSTEM'
                curdef = sys_m.group(1)
                continue
        
            if mode == 'LIBDISK':
                l.write(line)
            elif mode == 'FF':
                f.write(line)
            elif mode == 'DISKDEF':
                d.write(line)
            elif mode == '22DISK':
                two.write(line)

except Exception as e:
    print(e)
    print("linenum: %d" % linenum)
    
            
