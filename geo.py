import geopandas as g
import pandas as p
import numpy as np
import subprocess
import sys
import matplotlib.pyplot as plt
import pvfdefaults as pvfd
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
import shapely

#use wikipedia
#location = sys.argv[1]
def wikiGeocoder(location):
	o = subprocess.getoutput("./geocode.sh " + location)
	if o == '  </head>':
		o = subprocess.getoutput('./geocode.sh "' + location +' mandal"') # then try ', Anantapur', and then ', Andhra'
		print('retried appending mandal')

	print(location, o)

def geopandasGeocoder(location):
	gm = g.tools.geocode(mandals)
	# gm = gm.append(g.tools.geocode(mandas[10:25]))

# Process of manually fixing mistakes eg if Agali is not found, try again with ', Anatapur' appended
# tmp=g.tools.geocode('Agali, Anantapur')
# tmp['mandal']='Agali'
# gm=gm.append(tmp, ignore_index=True)

# wikilocs = p.read_csv("locdb.wikipedia", header=None, comment='#', dtype={0: str, 1: np.float64, 2:np.float64})
# gdf = g.GeoDataFrame(wikilocs, geometry=g.points_from_xy(wikilocs[2], wikilocs[1]))
# #here 2 values had to be dropped cause they werent found in wiki and were set to 0,0
# #Atmakur and O D Cheruvu
# gdf.drop(4, axis=0, inplace=True)
# gdf.drop(38, axis=0, inplace=True)

class meta:
	def __init__(self, e, lc, gf, glc):
		self.electedas=e
		self.locCol=lc
		self.geoFile=gf
		self.geolocCol=glc
		self.geoDataFrame = g.GeoDataFrame()
		self.data = None

	def gdf(self):
		if self.geoDataFrame.empty:
			self.geoDataFrame = g.read_file(self.geoFile)
			self.geoDataFrame[self.geolocCol] = self.geoDataFrame[self.geolocCol].str.title()
		return self.geoDataFrame

	def reconcile_names(self):
		# find mandals with unset parties and reset names with variants. 
		self.geoDataFrame.loc[self.geoDataFrame.party == 'NA',self.geolocCol]=self.geoDataFrame[self.geoDataFrame.party == 'NA'][self.geolocCol].apply(lambda x: x if pvfd.getSpellingVariants(x) is None else pvfd.getSpellingVariants(x)[0].strip())

	# adding/updating party column
	# reconcile data file with geo file. names may mismatch due to spellings or they maybe missing
	# only plot if lat long are known
	def updateColumnToPlot(self, d):
	    #drop party column if it exists
	    if 'party' in self.geoDataFrame:
	        self.geoDataFrame.drop('party', axis=1, inplace=True)
	    print('update ',len(d))
	    for i in self.geoDataFrame.index:
	        if self.geoDataFrame.loc[i][self.geolocCol] in d[self.locCol].to_list():
	            self.geoDataFrame.loc[i,'party'] = d[d[self.locCol] == self.geoDataFrame.loc[i][self.geolocCol]]['party'].values[0]
	        else:
	            self.geoDataFrame.loc[i,'party'] = 'NA'
	    self.data = d

	def queryFilteredData(self, location):
		return self.data[self.data[self.locCol] == location]

class ElecData():
	def __init__(self, filename):
		self.data = p.read_csv(filename)
	def get(self, year, electype):
		return self.data[(self.data['year']==year) & (self.data['electedas'].str.startswith(electype.electedas))]

data = ElecData('data/rep.csv')

zptc=meta('ZPTC','mandal','mandals_gj.json','mandalnam')
mptc=meta('MPTC','area','gp_gj.json', 'villagenam') #'grmpchnam'
mptc2=meta('MPTC','area','villages_gj.json', 'villagenam')

colors = {'BJP':'orange', 'CPI(M)':'red', 'Independent': 'purple',
'IND': 'purple','INC':'green', 'TDP':'yellow', 'dentTDP':'yellow', 
'CPI':'red', 'NA':'black', 'YSRCP':'blue'}

def rowsUnset():
	print(df[df.party=='NA'][context.geolocCol])

# add location name to plot
def annotate_centroid(ax):
	for x,y, label in zip(df.geometry.centroid.x, df.geometry.centroid.y , df[context.geolocCol]):
		ax.annotate(label, xy=(x,y), xytext=(3,3), textcoords="offset points")
#use if using locdb which just has x,y and not shapes
def annotate_xy(ax):
	for x,y, label in zip(df.geometry.x, df.geometry.y , df[context.geolocCol]):
		ax.annotate(label, xy=(x,y), xytext=(3,3), textcoords="offset points")

class UIControl(object):
	year_index = 0
	level = 0
	ptype = 0
	def zoom(self, event):
		self.level += 1
		i = self.level % len(hierachy)
		global context
		context = hierachy[i]
		print(len(context.gdf()))
		shapes()
	def next(self, event):
		self.year_index += 1
		i = self.year_index % len(years)
		d=data.get(years[i], context)
		context.updateColumnToPlot(d)
		shapes()
		#print(d.year.values[0])
		#reconcile_names()
	def style(self, event):
		self.ptype +=1
		ptype[self.ptype % len(ptype)]()

def shapes(annotate=False, customColor=True):
	global f,ax
	ax.set_title(context.electedas + ' '+ str(year))
	#for hover handling
	#f.canvas.mpl_connect('motion_notify_event', onclick2)
	patches = []
	cats = []
	df=context.gdf()
	if customColor:
		for i in df.party.unique():
			h=df[df.party == i]
			g.plotting.plot_polygon_collection(ax, h.geometry, facecolor=colors[i], edgecolor='gray', label=i)
			patches.append(
                    Line2D([0], [0], linestyle="none", 
                    	marker="o",
                        markersize=10,
                        markerfacecolor=colors[i],
                        markeredgewidth=0))
			cats.append(i)
			legend_kwds = {}
			legend_kwds.setdefault('numpoints', 1)
			legend_kwds.setdefault('loc', 'best')
		ax.legend(patches, cats, **legend_kwds)
		#ax.legend()	
	else:
		df.plot(ax=ax,column='party', categorical=True, legend=True)
	if annotate:
		annotate_centroid(ax)
	global annote
	#annote = ax.annotate("", xy=(0,0), xytext=(-30,30), textcoords="offset points", 
	#							bbox=dict(boxstyle="round", fc="w"), 
	#							arrowprops=dict(arrowstyle="->"))
	annote = ax.annotate("", xy=(0.01,0.9), xycoords="figure fraction", 
								bbox=dict(boxstyle="round",fc='black'), 
								color='orange')
	
	annote.set_visible(False)	
	#plt.show()
	f.canvas.draw_idle()

# use points instead of shapes 
def plot_points(geolabel=False):
	ax.set_title(context.electedas + ' '+ str(year))
	# to get the colors to match a particular party and labels to match a particular color
	for i in df.party.unique():
		h=df[df.party == i]
		x=h.geometry.centroid.x
		y=h.geometry.centroid.y
		ax.scatter(x,y, c=colors[i], label=i)
	if geolabel:
		annotate_xy(ax)
	ax.legend()
	plt.show()

def onclick(event):
	axsub = event.inaxes
	print(event)
	if axsub:
		# since points are split by party into seperate pointcollections for legend to work
		# find which (party based) point collection has been clicked
		for pathCollection in allpc:
			yes, index = pathCollection.contains(event)
			if yes:
				update_annote(pathCollection, index)
				annote.set_visible(True)
				f.canvas.draw_idle()
				break

def onclick2(event):
	axsub = event.inaxes
	if axsub:
		global tmp
		df=context.gdf()
		tmp = df[df.contains(shapely.geometry.Point(event.xdata,event.ydata))]
		print('shape click '+tmp[context.geolocCol])
		if len(tmp)>0:
			#global annote
			#annote.xy = (event.xdata,event.ydata)
			loc = tmp[context.geolocCol].values[0]
			#print(loc)
			rep = context.queryFilteredData(loc)
			name = rep.name.values[0]
			party = rep.party.values[0]
			annote.set_text(loc + " "+name+" "+party)
			annote.set_visible(True)
			f.canvas.draw_idle()


def update_annote(pc, ind):
	pos = pc.get_offsets()[ind["ind"][0]]
	global annote
	annote.xy = pos
	party = pc.get_label()
	txt = df[df.party == party][context.geolocCol].values[ind["ind"][0]]
	#txt = ind["ind"][0]
	print(txt)
	name = d[d[context.locCol] == txt].name.values[0]
	#annote.set_text(party + "\n" + mandal + "\n" + name)
	annote.set_text(party + "\n" + txt+' '+name)
	#annote.get_bbox_patch().set_facecolor('black')

# when hovering over a mandal doaction - show info - excute script etc 
def points(annotate=False):
	global f,ax
	ax.set_title(context.electedas + ' '+ str(year))
	f.canvas.mpl_connect('button_press_event', onclick)
	#f.canvas.mpl_connect('motion_notify_event', hover)
	global allpc
	allpc = []
	df=context.gdf()
	for i in df.party.unique():
		h=df[df.party == i]
		x=h.geometry.centroid.x
		y=h.geometry.centroid.y
		allpc.append(ax.scatter(x,y, c=colors[i], label=i))
	if annotate:
		global annote
		annote = ax.annotate("", xy=(0,0), xytext=(-30,30), textcoords="offset points", 
								bbox=dict(boxstyle="round", fc="w"), 
								arrowprops=dict(arrowstyle="->"))
		annote.set_visible(False)
	ax.legend()
	f.canvas.draw_idle()

year=sys.argv[2] or 2001
years = [2001, 2006, 2014]
hierachy = [zptc, mptc]

context = zptc
print('loading', len(context.gdf()))
context.updateColumnToPlot(data.get(year, zptc))
ui = UIControl()
annote=None
tmp=None

# pathcollections
allpc=[]
annotes=[]
ptype = [shapes, points]

#f,ax = None, None
f,ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
ax.set_axis_off()
f.canvas.mpl_connect('button_press_event', onclick2)

axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(ui.next)

axzoom = plt.axes([0.7, 0.05, 0.1, 0.075])
zup = Button(axzoom, 'Zoom')
zup.on_clicked(ui.zoom)

axstyle = plt.axes([0.6, 0.05, 0.1, 0.075])
bstyle = Button(axstyle, 'Style')
bstyle.on_clicked(ui.style)

shapes()
plt.show()
