#!/usr/bin/python
import pandas as p
import re
import math
import random
import datetime
import sys
import os

m = p.read_csv('data/rep.csv')
# Initialize useful calculated fields:
# Total number of seats per number of rows in diagram:
Totals = [4, 15, 33, 61, 95, 138, 189, 247, 313, 388, 469, 559, 657, 762, 876, 997, 1126, 1263, 1408, 1560, 1722, 1889, 2066, 2250, 2442, 2641, 2850, 3064, 3289, 3519, 3759, 4005, 4261, 4522, 4794, 5071, 5358, 5652, 5953, 6263, 6581, 6906, 7239, 7581, 7929, 8287, 8650, 9024, 9404,
          9793, 10187, 10594, 11003, 11425, 11850, 12288, 12729, 13183, 13638, 14109, 14580, 15066, 15553, 16055, 16557, 17075, 17592, 18126, 18660, 19208, 19758, 20323, 20888, 21468, 22050, 22645, 23243, 23853, 24467, 25094, 25723, 26364, 27011, 27667, 28329, 29001, 29679, 30367, 31061]

colors = {'BJP':'orange', 'CPI(M)':'red', 'Independent': 'purple',
'IND': 'purple','INC':'green', 'INC(I)':'green', 'TDP':'yellow', 'dentTDP':'yellow', 
'CPI':'red','CPM':'pink', 'NA':'black', 'YSRCP':'blue', 'JNP':'#ff3388',
'Indepen':'purple'}

years = sorted(m.year.unique())
print(years)
#m=m.groupby(['year','name']).apply(lambda x: x.nlargest(1,'votes'))

if len(sys.argv) > 1 and int(sys.argv[1]) in years:
    yr = int(sys.argv[1])

partylist=m.query("electedas == 'MPTC' and year=="+str(yr))['party']
#partylist = m.loc[yr]['abr']
pcount=partylist.value_counts().to_dict()
# Keep a running total of the number of delegates in the diagram, for use later.
print(pcount)
sumdelegates = sum(pcount.values())
# error flag: This seems ugly, but what should I do?
error = 0

for i in range(len(Totals)):
    if Totals[i] >= sumdelegates:
        rows = i+1
        break
# Maximum radius of spot is 0.5/rows; leave a bit of space.
radius = 0.4/rows
# Open svg file for writing:
outfile = open(str(yr)+'.svg', 'w')
# Write svg header:
outfile.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
outfile.write('<svg xmlns:svg="http://www.w3.org/2000/svg"\n')
outfile.write('xmlns="http://www.w3.org/2000/svg" version="1.1"\n')
# Make 350 px wide, 175 px high diagram with a 5 px blank border
outfile.write('width="360" height="185">\n')
outfile.write('<!-- Created with the Wikimedia parliament diagram creator (http://tools.wmflabs.org/parliamentdiagram/parliamentinputform.html) -->\n')
outfile.write('<g>\n')
# Print the number of seats in the middle at the bottom.
outfile.write('<text x="175" y="175" style="font-size:36px;font-weight:bold;text-align:center;text-anchor:middle;font-family:sans-serif">'+str(sumdelegates)+'</text>\n')
# Create list of centre spots
poslist = []
for i in range(1, rows):
    # Each row can contain pi/(2asin(2/(3n+4i-2))) spots, where n is the number of rows and i is the number of the current row.
    # Fill each row proportionally to the "fullness" of the diagram, up to the second-last row.
    J = int(float(sumdelegates) / Totals[rows-1] * math.pi/(2*math.asin(2.0/(3.0*rows+4.0*i-2.0))))
    # The radius of the ith row in an N-row diagram (Ri) is (3*N+4*i-2)/(4*N)
    R = (3.0*rows+4.0*i-2.0)/(4.0*rows)
    if J == 1:
        poslist.append([math.pi/2.0, 1.75*R, R])
    else:
        for j in range(J):
            # The angle to a spot is n.(pi-2sin(r/Ri))/(Ni-1)+sin(r/Ri) where Ni is the number in the arc
            # x=R.cos(theta) + 1.75
            # y=R.sin(theta)
            angle = float(j) * \
                    (math.pi-2.0*math.sin(radius/R)) / \
                    (float(J)-1.0)+math.sin(radius/R)
            poslist.append([angle, R*math.cos(angle)+1.75, R*math.sin(angle)])
# Now whatever seats are left go into the outside row:
J = sumdelegates-len(poslist)
R = (7.0*rows-2.0)/(4.0*rows)
if J == 1:
    poslist.append([math.pi/2.0, 1.75*R, R])
else:
    for j in range(J):
        angle = float(j) * \
                (math.pi-2.0*math.sin(radius/R)) / \
                (float(J)-1.0)+math.sin(radius/R)
        poslist.append([angle, R*math.cos(angle)+1.75, R*math.sin(angle)])
poslist.sort(reverse=True)
Counter = -1  # How many spots have we drawn?
for i in pcount:
    # Make each party's blocks an svg group
    outfile.write('  <g style="fill:'+colors[i]+'; stroke:' +
                  colors[i]+'" id="'+i+'">\n')
    for Counter in range(Counter+1, Counter+pcount[i]+1):
        tempstring = '    <circle cx="%.2f" cy="%.2f" r="%.2f"/>' % (
            poslist[Counter][1]*100.0+5.0, 100.0*(1.75-poslist[Counter][2])+5.0, radius*100.0)
        outfile.write(tempstring+'\n')
    outfile.write('  </g>\n')
outfile.write('</g>\n')
outfile.write('</svg>\n')
outfile.close()
# Pass the output filename to the calling page.
print('done')
