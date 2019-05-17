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

wikilocs = p.read_csv("locdb.wikipedia", header=None, comment='#', dtype={0: str, 1: np.float64, 2:np.float64})
gdf = g.GeoDataFrame(wikilocs, geometry=g.points_from_xy(wikilocs[2], wikilocs[1]))
#here 2 values had to be dropped cause they werent found in wiki and were set to 0,0
#Atmakur and O D Cheruvu
gdf.drop(4, axis=0, inplace=True)
gdf.drop(38, axis=0, inplace=True)

colors = {'BJP':'orange', 'IND': 'purple','INC':'green', 'TDP':'yellow', 'CPI':'red', 'NA':'black', 'YSRCP':'blue'}

def plotzp_geopandas(file, annotate=False):
	zptc = p.read_csv(file)
	for i in gdf.index:
		if gdf.loc[i][0] in zptc.mandal.to_list():
			gdf.loc[i,'party'] = zptc[zptc.mandal == gdf.loc[i][0]]['party'].values[0]
		else:
			gdf.loc[i,'party'] = 'NA'
	ax=gdf.plot(column='party', categorical=True, legend=True, c=gdf.party.apply(lambda x:colors[x]))	
	if annotate:
		for x,y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf[0]):
			ax.annotate(label, xy=(x,y), xytext=(3,3), textcoords="offset points")
	plt.show()

# use matplotlib 
def plotzp(file, annotate=False):
	#drop party column if it exists
	if 'party' in gdf:
		gdf.drop('party', axis=1, inplace=True)
	zptc = p.read_csv(file)
	# reconcile data file with geo file. names may mismatch due to spellings or they maybe missing
	# only plot if lat long are known
	for i in gdf.index:
		if gdf.loc[i][0] in zptc.mandal.to_list():
			gdf.loc[i,'party'] = zptc[zptc.mandal == gdf.loc[i][0]]['party'].values[0]
		else:
			gdf.loc[i,'party'] = 'NA'
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
	#drop party column if it exists
	if 'party' in gdf:
		gdf.drop('party', axis=1, inplace=True)
	zptc = p.read_csv(file)
	# reconcile data file with geo file. names may mismatch due to spellings or they maybe missing
	# only plot if lat long are known
	for i in gdf.index:
		if gdf.loc[i][0] in zptc.mandal.to_list():
			gdf.loc[i,'party'] = zptc[zptc.mandal == gdf.loc[i][0]]['party'].values[0]
		else:
			gdf.loc[i,'party'] = 'NA'
	#ax=gdf.plot(column='party', categorical=True, legend=True, c=gdf.party.apply(lambda x:colors[x]))	
	f,ax = plt.subplots()
	ax.set_axis_off()
	ax.set_title(file)
	
	#for i in gdf.index:
	#	ax.scatter(gdf.loc[i, 'geometry'].x, gdf.loc[i, 'geometry'].y, c=colors[gdf.loc[i, 'party']] )
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


plotzp_legends('apur_zptc_2001.csv')
plotzp_legends('apur_zptc_2006.csv')
plotzp_legends('apur_zptc_2014.csv')		