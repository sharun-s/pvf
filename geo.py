import geopandas as g
import subprocess
import sys

# mandas = [n for n, g in pdf.groupby('mandal')]
# gm = g.tools.geocode(mandas)
# type(g)
# import geopandas as ge
# gm = ge.tools.geocode(mandas)
# gm = ge.tools.geocode(mandas[:4])
# gm
# gm1 = ge.tools.geocode(mandas[4:10])
# gm2
location = sys.argv[1]
o = subprocess.getoutput("./geocode.sh " + location)
if o == '  </head>':
	o = subprocess.getoutput('./geocode.sh "' + location +' mandal"') # then try ', Anantapur', and then ', Andhra'
	print('retried appending mandal')

print(location, o)
# gm1.crs
# len(mandas)
# gm2 = ge.tools.geocode(mandas[10:25])
# gm2
# gm2 = ge.tools.geocode(mandas[10:15])
# gm3 = ge.tools.geocode(mandas[15:20])
# gm3 = ge.tools.geocode(mandas[15:18])
# gm3
# gm.plot()
# from matplotlib import pyplot
# gm.plot()
# from matplotlib import pyplot
# pyplot.show()
# gm + gm1
# gm.append(gm1)
# gm
# gm = gm.append(gm1)
# gm = gm.append(gm2))
# gm = gm.append(gm2)
# gm = gm.append(gm3)
# gm.plot()
# pyplot.show()
# gm
# gm.loc[1]
# gm.loc[Estonia]
# gm['address'=='Plli']
# gm[gm['address'].str.match('Plli')]
# gm[gm['address'].str.match('Plli')].drop()
# gm[gm['address'].str.match('Plli')].drop(1)
# gm
# gm.size()
# gm.size
# gm.rows
# gm.count()
# gm
# gm1
# gm2
# gm2.drop(1)
# #gm2 = ge.tools.geocode(mandas[10:15])
# mandas[10:15]
# o = subprocess.getoutput("./pvf/geocode.sh C.K.Palli")
# o
# o = subprocess.getoutput("./pvf/geocode.sh 'CK Palli'")
# o
# del mandas[11]
# mandas[10:15]
# gm = ge.tools.geocode(mandas[:18])
# gm
# gm.plot()
# pyplot.show()
# gm['address'].str.split(',').str[0]
# ax = gm.plot()
# for x,y, label in zip(gm.geometry.x, gm.geometry.y, gm.
# )
# gm.address.str.split(',').str[0]
# for x,y, label in zip(gm.geometry.x, gm.geometry.y, gm.address.str.split(',').str[0]):
# 	ax.annotate(label, xy=(x,y), xytext==(3,3), textcoords"offset points")
# 	ax.annotate(label, xy=(x,y), xytext==(3,3), textcoords="offset points")
# for x,y, label in zip(gm.geometry.x, gm.geometry.y, gm.address.str.split(',').str[0]):
# 	ax.annotate(label, xy=(x,y), xytext==(3,3), textcoords="offset points")
# for x,y, label in zip(gm.geometry.x, gm.geometry.y, gm.address.str.split(',').str[0]):
# 	ax.annotate(label, xy=(x,y), xytext=(3,3), textcoords="offset points")
# plt.show()
# pyplt.show()
# pyplot.show()
