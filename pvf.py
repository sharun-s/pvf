import csv, sys
#import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pprint import pprint

#fullheader 0year 1no 2name 3cat 4cname 5sex 6party 7abr 8votes 9tot -> pc
#newhdr 0year  2->1name  4->2cname 5->3sex 6->4party(notused) 7->5abr 8->6votes 9->7tot -> laptop
with open('apur.tsv', 'r') as nodecsv:
    nodereader = csv.reader(nodecsv, delimiter='\t')
    nodes = [n for n in nodereader][1:]

year_str ='1978'
def eq(value, idx):
    return [i for i in nodes if i[idx] == str(value)]

def like(value, idx):
    return [i for i in node if i[idx].find(x)>-1]

def s(results):
    for i in results:
        print('{0:4} {1:>20} {2:>28} {5:>8} {6:>8} {7:>8}'.format(*i) +' '+ '{:.2f}'.format(float(i[6])/float(i[7])*100))

votes=lambda j:[int(i[6]) for i in eq(year_str,0) if i[1].find(j)>-1]
orientation=lambda j:[partyangle[i[5]] for i in eq(year_str,0) if i[1].find(j)>-1]
pcolors=lambda j:[partycolor[i[5]] for i in eq(year_str,0) if i[1].find(j)>-1]

dgrid = {'Uravakonda':(0, 8), 
         'Guntakal': (4, 8), 
         'Tadipatri': (8,8),
         'Rayadurg':(0, 4), 
         'Anantapur Urban':(4, 4), 
         'Singanamala':(8, 4),
         'Kalyandurg':(0, 0)
}

ac=[(i[1],i[5],i[6]) for i in eq(year_str, 0)]
pprint(ac)

parties = set([i[1] for i in ac])
#pprint(parties)
plt.set_cmap(cm.Paired)

partyangle={'INC(I)':90, 'JNP':0, 'INC':30, 'TDP':20,
            'IND':270, 'CPI':180, 'BJP':325, 'MIM':260, 
            'DMM': 280, 'BSP': 250, 'SP':290, 'PPOI':240, 
            #1999 onwards
            'ATDP':300, 'NTRTDP(LP)':310, 'MCPI(S)':190, 'CPM':200,
            'BJRP':320, 'CPI(ML)(L)':210,
            'TPPP':220, 'PRAP':230, 'BHSASP':330, 'LSP':340, 'RDHP':345, 'PP':325, 
            'RPS':305, 'NOTA':0, 'JASPA':315, 'YSRCP':135, 'AAAP':355, 'STR':205, 'AIMIM':260, 'BCUF':215, 'SUCI':225, 'WPOI':295, 'MASP':270}
# increasing the highest value will change all other colors
# look at matplotlib.org colormap references for different colormaps
partycolor={'INC(I)': 3, 'INC':2, 'JNP':6.5, 'TDP':10, 
            'IND': 11, 'CPI': 5, 'BJP':8, 'MIM':3, 
            'DMM':11, 'BSP':4,'SP':11, 'PPOI':11, 
            'ATDP':10, 'NTRTDP(LP)':10, 'MCPI(S)':5, 'CPM':5,
            'BJRP':11, 'CPI(ML)(L)':5,
            'TPPP':11, 'PRAP':11, 'BHSASP':11, 'LSP':11, 'RDHP':11, 'PP':11, 
            'RPS':11, 'NOTA':1, 'JASPA':11, 'YSRCP':0, 'AAAP':11, 'STR':11, 'AIMIM':3, 'BCUF':11, 'SUCI':11, 'WPOI':11, 'MASP':11}
#pprint(parties)
#print(len(partycolor.keys()))
#print(len(parties))
#if len(partycolor.keys()) != len(parties):
#  sys.exit()

# this was old code when dgrid was split up as a 2d struct
#U = [list(map(votes, i)) for i in dgrid]
U = [votes(i) for i in dgrid]
largest = max(list(map(len, U)))
for i in U:
  while len(i) < largest:
    i.insert(0,0)
#pprint(U)

phi = [orientation(i) for i in dgrid]
largest = max(list(map(len, phi)))
for i in phi:
  while len(i) < largest:
    i.insert(0,0.)
#pprint(phi)

C = [pcolors(i) for i in dgrid]
largest = max(list(map(len, C)))
for i in C:
  while len(i) < largest:
    #i.insert(0,(1.0,1.0,1.0))
    i.insert(0,0.)
#pprint(C)
X=[ dgrid[i][0] for i in dgrid for j in range(0,largest)] 

Y=[ dgrid[i][1] for i in dgrid for j in range(0,largest)]

q=plt.quiver( X, Y, 
           U,
           [0],
           C,
           #headlength=0.25, headaxislength=0.25,
           #headwidth=1,
           angles=phi,
           #scale_units='width',
           #color=['w', 'w', 'k', 'r', 'g', 'b']
           )

for i in dgrid:
  plt.quiverkey(q, dgrid[i][0], dgrid[i][1], len(i), i,
                      labelpos='S', coordinates = 'data')
plt.axes().set_axis_off()
#plt.xlim(-30, 30)
#plt.ylim(-2, 30)
plt.ylim(-1,12)
plt.xlim(-1,12)
plt.show()
