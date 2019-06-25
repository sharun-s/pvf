import geopandas as g
import pandas as p
import numpy as np
import subprocess
import sys
import matplotlib.pyplot as plt

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
	def __init__(self, e, lc, g, glc):
		self.electedas=e
		self.locCol=lc
		self.geoFile=g
		self.geolocCol=glc

colors = {'BJP':'orange', 'CPI(M)':'red', 'Independent': 'purple',
'IND': 'purple','INC':'green', 'TDP':'yellow', 
'CPI':'red', 'NA':'black', 'YSRCP':'blue'}

data=p.read_csv('data/rep.csv')

zptc=meta('ZPTC','mandal','mandals_gj.json','mandalnam')
mptc=meta('MPTC','area','gp_gj.json', 'villagenam') #'grmpchnam'
mptc2=meta('MPTC','area','villages_gj.json', 'villagenam')

year=sys.argv[2] or 2001

def setup(m=zptc):
	df=g.read_file(m.geoFile)
	df[m.geolocCol] = df[m.geolocCol].str.title()
	d=data[(data['year']==year) & (data['electedas'].str.startswith(m.electedas))]
	return m,df,d

context,df,d=setup()

import pvfdefaults as pvfd

def reconcile_names():
	# find mandals with unset parties and reset names with variants. 
	df.loc[df.party == 'NA',context.geolocCol]=df[df.party == 'NA'][context.geolocCol].apply(lambda x: x if pvfd.getSpellingVariants(x) is None else pvfd.getSpellingVariants(x)[0].strip())

# reconcile data file with geo file. names may mismatch due to spellings or they maybe missing
# only plot if lat long are known
def addPartyCol():
	#drop party column if it exists
	if 'party' in df:
		df.drop('party', axis=1, inplace=True)
	for i in df.index:
		if df.loc[i][context.geolocCol] in d[context.locCol].to_list():
			df.loc[i,'party'] = d[d[context.locCol] == df.loc[i][context.geolocCol]]['party'].values[0]
		else:
			df.loc[i,'party'] = 'NA'	

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

def plot_shapes(annotate=False, customColor=True):
	addPartyCol()
	global f,ax
	f,ax = plt.subplots()
	ax.set_axis_off()
	ax.set_title(context.electedas + ' '+ str(year))
	f.canvas.mpl_connect('button_press_event', onclick2)
	
	if customColor:
		df.plot(ax=ax,column='party', categorical=True, legend=True, color=df.party.apply(lambda x:colors[x]), edgecolor='red')	
	else:
		df.plot(ax=ax,column='party', categorical=True, legend=True)
	if annotate:
		annotate_centroid(ax)
	global annote
	annote = ax.annotate("", xy=(0,0), xytext=(-30,30), textcoords="offset points", 
								bbox=dict(boxstyle="round", fc="w"), 
								arrowprops=dict(arrowstyle="->"))
	annote.set_visible(False)	
	plt.show()

# use matplotlib 
def plot_points(annotate=False):
	addPartyCol()
	#ax=gdf.plot(column='party', categorical=True, legend=True, c=gdf.party.apply(lambda x:colors[x]))	
	f,ax = plt.subplots()
	ax.set_axis_off()
	ax.set_title(context.electedas + ' '+ str(year))
	ax.scatter(df.geometry.centroid.x, df.geometry.centroid.y, c = df.party.apply(lambda x:colors[x]) , edgecolor='black')
	if annotate:
		annotate_centroid(ax)
	ax.legend()
	plt.show()

# use matplotlib 
def plot_points_legends(annotate=False):
	addPartyCol()
	f,ax = plt.subplots()
	ax.set_axis_off()
	ax.set_title(context.electedas + ' '+ str(year))
	# to get the colors to match a particular party and labels to match a particular color
	for i in df.party.unique():
		h=df[df.party == i]
		x=h.geometry.centroid.x
		y=h.geometry.centroid.y
		ax.scatter(x,y, c=colors[i], label=i)
	if annotate:
		annotate_xy(ax)
	ax.legend()
	plt.show()

annote=None

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
import shapely
tmp=None
def onclick2(event):
	axsub = event.inaxes
	if axsub:
		global tmp
		tmp = df[df.contains(shapely.geometry.Point(event.xdata,event.ydata))]
		if len(tmp)>0:
			global annote
			annote.xy = (event.xdata,event.ydata)
			loc = tmp.iloc[0][context.geolocCol]
			name = d[d[context.locCol] == loc].name.values[0]
	
			annote.set_text(tmp.iloc[0]['party'] + "\n"+name+"\n" + tmp.iloc[0][context.geolocCol])
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

# pathcollections
allpc=[]
annotes=[]
# def hover(event):
# 	axsub = event.inaxes
# 	if axsub:
# 		# since points are split by party into seperate pointcollections for legend to work
# 		# find which (party based) point collection has been clicked
# 		for j in allpc:
# 			cnt, ind = j.contains(event)
# 			if cnt:
# 				#print(ind["ind"][0])
# 				update_annote(j, ind)
# 				annote.set_visible(True)
# 				f.canvas.draw_idle()
# 				break

# when hovering over a mandal doaction - show info - excute script etc 
def plot_legends_ux(annotate=False):
	addPartyCol()
	global f, ax
	f,ax = plt.subplots()
	ax.set_axis_off()
	ax.set_title(context.electedas + ' '+ str(year))
	f.canvas.mpl_connect('button_press_event', onclick)
	#f.canvas.mpl_connect('motion_notify_event', hover)
	global allpc
	allpc = []
	#for i in gdf.index:
	#	ax.scatter(gdf.loc[i, 'geometry'].x, gdf.loc[i, 'geometry'].y, c=colors[gdf.loc[i, 'party']] )
	# to get the colors to match a particular party and labels to match a particular color
	for i in df.party.unique():
		h=df[df.party == i]
		x=h.geometry.centroid.x
		y=h.geometry.centroid.y
		allpc.append(ax.scatter(x,y, c=colors[i], label=i))
	
	if annotate:
		#for j in allpc:
		global annote
		annote = ax.annotate("", xy=(0,0), xytext=(-30,30), textcoords="offset points", 
								bbox=dict(boxstyle="round", fc="w"), 
								arrowprops=dict(arrowstyle="->"))
		annote.set_visible(False)
		#annotes.append(annote)

	#annot_dict = dict(zip(allpc, annotes))
	#ax_dict = dict(zip(allax, allax))

	ax.legend()
	plt.show()


f,ax = None, None

