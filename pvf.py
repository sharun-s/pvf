import csv, sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pprint import pprint
from math import ceil, sqrt


# used along with largest vote count to determine size of a cell(location) in a square grid
votesperinch= 10000/0.25
# group parlimentary, assembly plots
combinePlots=False
  
#fullheader 0year 1no 2name 3cat 4cname 5sex 6party 7abr 8votes 9tot -> pc
#newhdr 0year  2->1name  4->2cname 5->3sex 6->4party(notused) 7->5abr 8->6votes 9->7tot -> laptop
with open('apur.tsv', 'r') as nodecsv:
    nodereader = csv.reader(nodecsv, delimiter='\t')
    nodes = [n for n in nodereader][1:]

def eq(value, idx):
    return [i for i in nodes if i[idx] == str(value)]

def like(value, idx):
    return [i for i in node if i[idx].find(x)>-1]

def show(results):
    for i in results:
        print('{0:4} {1:>20} {2:>28} {5:>8} {6:>8} {7:>8}'.format(*i) +' '+ '{:.2f}'.format(float(i[6])/float(i[7])*100))

def pad(array2D, value):
  length_of_longestmember = max(list(map(len, array2D)))
  for i in array2D:
    while len(i) < length_of_longestmember:
      i.insert(0, value)
  #pprint(array2D)
  return length_of_longestmember

partyangle={'INC(I)':90, 'JNP':0, 'INC':30, 'TDP':20, 'BLD':5,'JP':10, 'ICSP':300,
            'IND':270, 'CPI':180, 'BJP':325, 'MIM':260, 'CPI(ML)':190, 'TRS':270,
            'DMM': 280, 'BSP': 250, 'SP':290, 'PPOI':240, 
            #1999 onwards
            'ATDP':300, 'NTRTDP(LP)':310, 'MCPI(S)':190, 'CPM':200,
            'BJRP':320, 'CPI(ML)(L)':210, 
            'TPPP':220, 'PRAP':230, 'BHSASP':330, 'LSP':340, 'RDHP':345, 'PP':325, 
            'RPS':305, 'NOTA':0, 'JASPA':315, 'YSRCP':135, 
            'AAAP':355, 'STR':205, 'AIMIM':260, 'BCUF':215, 
            'SUCI':225, 'WPOI':295, 'MASP':270, 'JaSPa':315}
# increasing the highest value will change all other colors
# look at matplotlib.org colormap references for different colormaps
partycolor={'INC(I)': 3, 'INC':2, 'JNP':6.5, 'TDP':10, 'BLD':10,'JP':10, 'ICSP':11,
            'IND': 11, 'CPI': 5, 'BJP':8, 'MIM':3, 'CPI(ML)':5, 'TRS':11,
            'DMM':11, 'BSP':4,'SP':11, 'PPOI':11, 
            'ATDP':10, 'NTRTDP(LP)':10, 'MCPI(S)':5, 'CPM':5,
            'BJRP':11, 'CPI(ML)(L)':5,
            'TPPP':11, 'PRAP':11, 'BHSASP':11, 'LSP':11, 'RDHP':11, 'PP':11, 
            'RPS':11, 'NOTA':1, 'JASPA':11, 'YSRCP':0, 
            'AAAP':11, 'STR':11, 'AIMIM':3, 'BCUF':11, 
            'SUCI':11, 'WPOI':11, 'MASP':11, 'JaSPa':11}
#pprint(dgrid)
#parties = set([i[1] for i in results])
#pprint(parties)

#pprint(parties)
#print(len(partycolor.keys()))
#print(len(parties))
#if len(partycolor.keys()) != len(parties):
#  sys.exit()

# for parlimentary elections (MP) only one location needs to be plotted
# for assembly elections (MLAs) 7 locations need to be plotted
# some years both elections happen grid must be approriately reshapped 
# TODO: doing this right requires a election type column in the data
# that would support all 5 levels of elections - 
# 1 - MP, 2 - MLA, 3 - Zila Parishad/MuniCorp, 4 - Mandal/Taluk/Tehsil, 5 - GramPanchayat/Ward
def selectgrid(locations):
  if len(locations) ==1:
    return computeLayout(['Anantapur'])
  elif len(locations)==7:
    return computeLayout(['Uravakonda', 'Guntakal', 'Tadipatri', 'Rayadurg', 'Anantapur Urban', 'Singanamala', 'Kalyandurg'])
    # return {'Uravakonda':(0, ymax-border-(groupspace/2)), 
    #      'Guntakal': (xmax/2,  ymax-border-(groupspace/2)), 
    #      'Tadipatri': (xmax-border, ymax-border-(groupspace/2)),
    #      'Rayadurg':(0, (ymax/2)-border), 
    #      'Anantapur Urban':(xmax/2, ymax/2-border),
    #      'Singanamala':(xmax-border, ymax/2-border),
    #      'Kalyandurg':(0, 0)
    #      }, xmax, ymax
  else:
    gridrows = 8
    groupspace= 4 #2x2
    xmax = gridrows * groupspace
    ymax = gridrows * groupspace
    return {
        'Anantapur':(16, 24),
         'Uravakonda':(6, 15), 
         'Guntakal': (16, 15), 
         'Tadipatri': (24, 15),
         'Rayadurg':(6, 7), 
         'Anantapur Urban':(16, 7), 
         'Singanamala':(24, 7),
         'Kalyandurg':(6, 0)
    }, xmax, ymax

# currently using hardcoded data until datafiles include 
# electiontype col - MP, MLA, ZLTC, MLTC, Panchayat, Ward
electiontype={'Anantapur':'MP', 
'Uravakonda':'MLA','Guntakal':'MLA','Tadipatri':'MLA',
'Rayadurg':'MLA', 'Anantapur Urban':'MLA', 'Singanamala':'MLA',
'Kalyandurg':'MLA'}
def splitLocationsByType(locations):
  breakup = {}
  for i in locations:
    if electiontype[i] in breakup:
      breakup[electiontype[i]].append(i)
    else:
      breakup[electiontype[i]] = [i]
  return breakup.values()


# For 10000 votes to correspond to 1/4 inch
# set votestoinch ratio u = 10000/.25
# So 100000 votes occupies 2.5 inches
# M = max votes in all cells (cause max needs to fit within a cell)
# half height/width of a cell = M/u eg 200000 * .25/10000 = 5inchs  
# total cell space is then 2*5, 2*5 or 10 by 10 with 0,0 in the center
# cellwidth = cellheight = 2*M*u
# now if L = number of locations eg 7
# they must be mapped into the square grid 
# in square grid rows = columns   
# so to find ideal R,C => ceil(sqrt(L)) eg for 7 locations we get 3 for 3x3 grid 
# now find the x, y or origin of each cell given r,c
# maxx = maxy = R*cellwidth
# calc origins = array of center point of each cell specified by Location array
# 1st element maps to northwest or topleft corner of grid the move left to right - top down
# so index in Locations array will determine positions 
def computeLayout(Locations):
  U = [votes(i) for i in Locations]
  #print(U)
  LargestVoteCount = max(max([i for i in U]))
  #print(LargestVoteCount)
  halfcell = int(ceil(LargestVoteCount * (1/votesperinch))) 
  LocationCount = len(Locations)
  # uniform square grid where cellwidth = cellheigth
  cellwidth = 2* halfcell
  R = ceil(sqrt(LocationCount))
  maxx = maxy = R*cellwidth
  origins = [ (j+halfcell, i-halfcell ) for i in range(maxx, 0, -1*cellwidth) for j in range(0,maxy,cellwidth)]
  dgrid={}
  for i,name in enumerate(Locations):
    dgrid[name]= origins[i]
  #print(dgrid, maxx, maxy)
  return dgrid, maxx, maxy

def plot(plt, dgrid, xmax, ymax):
  fig, ax = plt.subplots(1,1)
  # diff locations have different number of results
  # quiver seems(?) to require all num of vectors in each 
  # groups be the same. Currently padding with 0 to deal with this issue. 
  U = [votes(i) for i in dgrid]
  #pprint(U)
  pad(U, 0)

  plt.set_cmap(cm.Paired)
  
  phi = [orientation(i) for i in dgrid]
  pad(phi, 0.)

  C = [pcolors(i) for i in dgrid]
  newlength = pad(C, 0.)
  
  X=[ dgrid[i][0] for i in dgrid for j in range(0, newlength)]
  #print(X)
  Y=[ dgrid[i][1] for i in dgrid for j in range(0, newlength)]
  #print(list(zip(X,Y)))
  q=ax.quiver( X, Y, 
             U,
             [0],
             C,
             #headlength=0.25, headaxislength=0.25,
             #headwidth=1,
             #units='y',
             angles=phi, 
             scale_units='y', 
             scale=votesperinch
             #color=['w', 'w', 'k', 'r', 'g', 'b']
             )

  for i in dgrid:
    ax.quiverkey(q, dgrid[i][0], dgrid[i][1], len(i), i,
                        labelpos='S', coordinates = 'data')

  ax.set_axis_off()
  ax.set_title(year_str)
  ax.set_ylim(0, ymax)
  ax.set_xlim(0, xmax)
  
  if combinePlots:
    filename = year_str+'.png' 
  else:
    filename = year_str+'_'+electiontype[list(dgrid.keys())[0]]+'.png'
  fig.savefig(filename, format='png')  
#anim = animation.FuncAnimation(fig, update_quiver, fargs=(Q, X, Y),
#                               interval=50, blit=False)
  #fig.tight_layout()
  #plt.show()

years = sorted(set([i[0] for i in nodes]))
if len(sys.argv) > 1 and sys.argv[1] in years:
  years = [sys.argv[1]]

for year_str in years:
  print(year_str)
  results=[(i[1],i[5],i[6]) for i in eq(year_str, 0)]
  
  votes = lambda j:[int(i[6]) for i in eq(year_str,0) if i[1].find(j)>-1]
  orientation = lambda j:[partyangle[i[5]] for i in eq(year_str,0) if i[1].find(j)>-1]
  pcolors = lambda j:[partycolor[i[5]] for i in eq(year_str,0) if i[1].find(j)>-1]
  locations = set([i[0] for i in results])
  #pprint(locations)

  if combinePlots:  
    dgrid, xmax, ymax = selectgrid(locations)
    plot(plt, dgrid, xmax, ymax)
  else:
    for l in splitLocationsByType(locations):
      dgrid, xmax, ymax = selectgrid(l)
      plot(plt, dgrid, xmax, ymax)