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

colors = {'BJP':'orange', 'IND': 'purple','INC':'green', 'TDP':'yellow', 'CPI':'red', 'NA':'black', 'YSRCP':'blue'}

zptc=None
gdf=g.read_file('mandals_gj.json')
gdf.mandalnam = gdf.mandalnam.str.title()
import pvfdefaults as pvfd

def reconcile_names():
	# find mandals with unset parties and reset names with variants. 
	gdf.loc[gdf.party == 'NA','mandalnam']=gdf[gdf.party == 'NA'].mandalnam.apply(lambda x: x if pvfd.getSpellingVariants(x) is None else pvfd.getSpellingVariants(x)[0].strip())


def _addPartyColFrom(file):
	#drop party column if it exists
	if 'party' in gdf:
		gdf.drop('party', axis=1, inplace=True)
	global zptc
	zptc = p.read_csv(file)
	# reconcile data file with geo file. names may mismatch due to spellings or they maybe missing
	# only plot if lat long are known
	for i in gdf.index:
		if gdf.loc[i]['mandalnam'] in zptc.mandal.to_list():
			gdf.loc[i,'party'] = zptc[zptc.mandal == gdf.loc[i]['mandalnam']]['party'].values[0]
		else:
			gdf.loc[i,'party'] = 'NA'	

def addPartyColFrom(file):
	#drop party column if it exists
	if 'party' in gdf:
		gdf.drop('party', axis=1, inplace=True)
	global zptc
	zptc = p.read_csv(file)
	# reconcile data file with geo file. names may mismatch due to spellings or they maybe missing
	# only plot if lat long are known
	for i in gdf.index:
		if gdf.loc[i][0] in zptc.mandal.to_list():
			gdf.loc[i,'party'] = zptc[zptc.mandal == gdf.loc[i][0]]['party'].values[0]
		else:
			gdf.loc[i,'party'] = 'NA'


def plotzp_geopandas(file, annotate=False):
	addPartyColFrom(file)
	ax=gdf.plot(column='party', categorical=True, legend=True, c=gdf.party.apply(lambda x:colors[x]))	
	if annotate:
		for x,y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf[0]):
			ax.annotate(label, xy=(x,y), xytext=(3,3), textcoords="offset points")
	plt.show()

def _plotzp_geopandas(file, annotate=False):
	_addPartyColFrom(file)
	print(gdf[gdf.party=='NA'].mandalnam)
	reconcile_names()
	_addPartyColFrom(file)
	print(gdf[gdf.party=='NA'].mandalnam)
	
	ax=gdf.plot(column='party', categorical=True, legend=True)	
	if annotate:
		for x,y, label in zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y , gdf['mandalnam']):
			ax.annotate(label, xy=(x,y), xytext=(3,3), textcoords="offset points")
	plt.show()

# use matplotlib 
def plotzp(file, annotate=False):
	addPartyColFrom(file)
	#ax=gdf.plot(column='party', categorical=True, legend=True, c=gdf.party.apply(lambda x:colors[x]))	
	f,ax = plt.subplots()
	ax.set_axis_off()
	ax.set_title(file)
	ax.scatter(gdf.geometry.x, gdf.geometry.y, c = gdf.party.apply(lambda x:colors[x]) )
	if annotate:
		for x,y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf[0]):
			ax.annotate(label, xy=(x,y), xytext=(3,3), textcoords="offset points")
	ax.legend()
	plt.show()

# use matplotlib 
def plotzp_legends(file, annotate=False):
	addPartyColFrom(file)
	f,ax = plt.subplots()
	ax.set_axis_off()
	ax.set_title(file)
	# to get the colors to match a particular party and labels to match a particular color
	for i in gdf.party.unique():
		h=gdf[gdf.party == i]
		x=h.geometry.x
		y=h.geometry.y
		ax.scatter(x,y, c=colors[i], label=i)
	if annotate:
		for x,y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf[0]):
			ax.annotate(label, xy=(x,y), xytext=(3,3), textcoords="offset points")
	ax.legend()
	plt.show()

annote=None

def onclick(event):
	axsub = event.inaxes
	if axsub:
		# since points are split by party into seperate pointcollections for legend to work
		# find which (party based) point collection has been clicked
		for j in allpc:
			cnt, ind = j.contains(event)
			if cnt:
				#print(ind["ind"][0])
				update_annote(j, ind)
				annote.set_visible(True)
				f.canvas.draw_idle()
				break


def update_annote(j, ind):
	pos = j.get_offsets()[ind["ind"][0]]
	global annote
	annote.xy = pos
	party = j.get_label()
	mandal = gdf[gdf.party == party][0].values[ind["ind"][0]]
	print(mandal)
	name = zptc[zptc.mandal == mandal].name.values[0]
	annote.set_text(party + "\n" + mandal + "\n" + name)
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
def plotzp_legends_hover(file, annotate=False):
	addPartyColFrom(file)
	global f, ax
	f,ax = plt.subplots()
	ax.set_axis_off()
	ax.set_title(file)
	f.canvas.mpl_connect('button_press_event', onclick)
	#f.canvas.mpl_connect('motion_notify_event', hover)
	global allpc
	allpc = []
	#for i in gdf.index:
	#	ax.scatter(gdf.loc[i, 'geometry'].x, gdf.loc[i, 'geometry'].y, c=colors[gdf.loc[i, 'party']] )
	# to get the colors to match a particular party and labels to match a particular color
	for i in gdf.party.unique():
		h=gdf[gdf.party == i]
		x=h.geometry.x
		y=h.geometry.y
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
#plotzp_legends_hover('apur_zptc_2001.csv', True)
#plotzp_legends('apur_zptc_2006.csv')
#plotzp_legends('apur_zptc_2014.csv')		

_plotzp_geopandas('data/apur_zptc_2001.csv', True)
_plotzp_geopandas('data/apur_zptc_2006.csv', True)
_plotzp_geopandas('data/apur_zptc_2014.csv', True)