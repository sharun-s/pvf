import geopandas as g
import subprocess
import sys

location = sys.argv[1]
o = subprocess.getoutput("./geocode.sh " + location)
if o == '  </head>':
	o = subprocess.getoutput('./geocode.sh "' + location +' mandal"') # then try ', Anantapur', and then ', Andhra'
	print('retried appending mandal')

print(location, o)
# import matplotlib.pyplot as plt
# import geopandas as ge
# gm = ge.tools.geocode(mandas)
# gm = gm.append(g.tools.geocode(mandas[10:25]))
# for x,y, label in zip(gm.geometry.x, gm.geometry.y, gm.address.str.split(',').str[0]):
# 	ax.annotate(label, xy=(x,y), xytext=(3,3), textcoords="offset points")
# plt.show()

# wikilocs = p.read_csv("locdb", header=None, comment='#', dtype={0: str, 1: np.float64, 2:np.float64})
# gdf = g.GeoDataFrame(wikilocs, geometry=g.points_from_xy(wikilocs[2], wikilocs[1]))
# #here 2 values had to be dropped cause they werent found in wiki and were set to 0,0
# Atmakur and O D Cheruvu
# gdf.drop(4, axis=0, inplace=True)
# gdf.drop(38, axis=0, inplace=True)
# a=gdf.plot()
# for x,y,label in zip(gdf.geometry.x, gdf.geometry.y, gdf[0].astype(str)):
#    a.annotate(label, xy=(x,y), xytext=(3,3), textcoords="offset points")

# Process of manually fixing mistakes eg if Agali is not found, try again with ', Anatapur' appended
# tmp=g.tools.geocode('Agali, Anantapur')
# tmp['mandal']='Agali'
# gloc=gloc.append(tmp, ignore_index=True)