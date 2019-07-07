import geopandas as g
import matplotlib.pyplot as p 

class layer(object):
	def __init__(self, df, color, edgecolor, alpha, linewidth):
		self.geometry = df.geometry
		self.fc = color
		self.ec = edgecolor
		self.alpha = alpha
		self.lw = linewidth

l1 = g.read_file('pc_apur_hpur_gj.json')
l2 = g.read_file('ac_apur_gj.json')
l3 = g.read_file('mandals_gj.json')
l4 = g.read_file('gp_gj.json')

layers = [
	# layer(l2, 'white','red',.61, 2 ),
	# layer(l3, 'white','blue',.31, 1 ),
	# layer(l4, 'white','red',.21, .5),
	# layer(l1, 'white','green',.41, 3),
	layer(l2, 'white','blue',.61, 2 ),
	layer(l3, 'white','red',.31, 1.5 ),
	layer(l4, 'white','blue',.21, .8),
	layer(l1, 'white','red',.41, 3),
]


f,ax = p.subplots()
ax.set_axis_off()

for i in layers:
	g.plotting.plot_polygon_collection(ax, i.geometry,facecolor=i.fc,
		 edgecolor=i.ec, lw=i.lw, alpha=i.alpha)
p.show()