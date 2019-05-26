import pandas as p
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pprint import pprint
from math import ceil, sqrt
from matplotlib.colors import Normalize
from pvfdefaults import partycolor, partyangle, electiontype

norm = Normalize(vmin=0.0, vmax=11.0)
# used along with largest vote count to determine size of a cell(location) in a square grid
votesperinch= 5000/0.25
# group parlimentary, assembly plots
combinePlots=False
saveFile=True

# without the color hack adding a upper and lower value 
# of the max and min color in the partycolor array quiver 
# normalizes colors in the array to whatever max and min in the array(bug in matplotlib)
def pad(array2D, value, colorHack):
  length_of_longestmember = max(list(map(len, array2D)))
  for i in array2D:
    while len(i) < length_of_longestmember:
      i.insert(0, value)
  for i in array2D:  
    if colorHack:
      i.insert(0, 11.)
    else:  
      i.insert(0, 0.)
    i.insert(0, 0.)
  #pprint([len(i) for i in array2D]) 
  #pprint(array2D)
  return length_of_longestmember+2

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
  U = [votes(i).to_list() for i in Locations]
  print(U)
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

def showLegend(results, ax, q, xmax):
  xpos =10
  #parties = results.abr.unique()
  parties = results.loc[results.votes.nlargest(20).index].abr.unique()[:3]
  for i in parties:
    wc = cm.Paired(norm(partycolor[i]))  
    ax.annotate(i, xy=(xpos,2), 
                xycoords="axes points", 
                bbox=dict(boxstyle="round", fc=wc))
    xpos=xpos+45


def plot(plt, dgrid, xmax, ymax):
  fig, ax = plt.subplots(1,1)
  # diff locations have different number of results
  # quiver seems(?) to require all num of vectors in each 
  # groups be the same. Currently padding with 0 to deal with this issue. 
  U = [votes(i).to_list() for i in dgrid]
  #pprint(U)
  pad(U, 0, False)
  #pprint(U)
  plt.set_cmap(cm.Paired)
  
  phi = [orientation(i) for i in dgrid]
  pad(phi, 0., False)
  #pprint(phi)
  C = [pcolors(i) for i in dgrid]
  #pprint(C)
  newlength = pad(C, 11., True)
  #pprint(C)
  #C=[[(0.6980392156862745, 0.8745098039215686, 0.5411764705882353, 1.0)
  #    ,cm.Paired(5)]]
  #C=[cm.Paired(i) for i in C]
  #pprint(C)
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
  showLegend(results, ax, q, xmax);
  #ax.quiverkey(q, 1, 1, )  
  ax.set_axis_off()
  ax.set_title(year_str)
  ax.set_ylim(0, ymax)
  ax.set_xlim(0, xmax)
  #ax.legend()
  #fig.colorbar(q)
  #print(list(dgrid.keys()))
  fig.tight_layout()

  if saveFile:
    if combinePlots:
      filename = str(year_str)+'.png' 
    else:
      filename = str(year_str)+'_'+electiontype[list(dgrid.keys())[0]]+'.png'
    
    fig.savefig(filename, format='png')  
  #anim = animation.FuncAnimation(fig, update_quiver, fargs=(Q, X, Y),
  #                               interval=50, blit=False)
  
  #plt.show()

# Extraction of MP's and MLA's into a dataframe m
m = p.read_csv('apur.csv')
# extract a dataframe mptc for 2014
#from extractTC import mptc
#print('mptc ', len(mptc))
# extract corporators, Mayor, Dep Mayor of MuniCorp (Cities)
# extract councillors, Chairman, Vice Chair of Municipalities (Towns)
# all stored in a datafram ulb for 2014
#from extractULB import ulb 
#print('ulb', len(ulb))
#print('mp mla columns-',len(m.column), 
#  'rural local bodies',len(mptc.column), 
#  'urban local bodies',len(ulb.column))

# if a year is passed on command line only plot that year else all
years = sorted(m.year.unique())
if len(sys.argv) > 1 and int(sys.argv[1]) in years:
  years = [int(sys.argv[1])]

for year_str in years:
  print(year_str)
  results = m[m['year']==year_str][['name','abr','votes']]
  votes = lambda j: results[results.name.eq(j)].votes
  orientation = lambda j:[partyangle[i] for i in results[results.name.eq(j)].abr]
  pcolors = lambda j:[partycolor[i] for i in results[results.name.eq(j)].abr]
  locations = results.name.unique()
  # chose whether to plot different types of elections as single or seperate plots
  # depending on the number of election types and combinePlot flag
  # different grids are plotted. The number of cells depends on the number of locations
  if combinePlots:  
    dgrid, xmax, ymax = selectgrid(locations)
    plot(plt, dgrid, xmax, ymax)
  else:
    for l in splitLocationsByType(locations):
      dgrid, xmax, ymax = selectgrid(l)
      plot(plt, dgrid, xmax, ymax)