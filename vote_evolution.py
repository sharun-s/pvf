import matplotlib.pyplot as plt
import sys
import pandas as p
import matplotlib.cm as cm 
from pvfdefaults import partycolor
from math import ceil, sqrt

#from optparse import OptionParse
#parser = OptionParser()
#parser.add_option()

# arg1 - region name or partial segment name
# arg2 - party abr eg TDP INC CPI will draw just those 3, if none show all

l = len(sys.argv)

results = p.read_csv("apur.csv")

if sys.argv[1] == 'all':
	pt = results.pivot_table(index=['name','year'], columns='abr',values='votes', fill_value=0)
	regions = pt.index.levels[0]
	gridsize = ceil(sqrt(len(regions)))
	fig, axes = plt.subplots(gridsize, gridsize, frameon=False, sharex=True, sharey=True)
	idx=0
	for row in range(0,gridsize):
		for col in range(0,gridsize):
			idx = idx + 1
			print(idx)
			if idx < len(regions):
				if l > 2:
					C = [cm.Paired(partycolor[i]) for i in sys.argv[2:]]
					#pt.loc[regions[idx]].plot(kind='barh', stacked=True, ax=axes[row][col], legend=False)
					pt.loc[regions[idx]].plot.barh(y=sys.argv[2:], stacked=True, ax=axes[col][row], legend=False, color=C)
				else:
					C = [cm.Paired(partycolor[i]) for i in pt.loc[regions[idx]].columns]
					#pt.loc[regions[idx]].plot(kind='barh', stacked=True, ax=axes[row][col], legend=False)
					pt.loc[regions[idx]].plot.barh(stacked=True, ax=axes[col][row], legend=False, color=C)
				axes[col][row].set_title(regions[idx])
	fig.delaxes(axes[1][2])
	fig.delaxes(axes[2][2])
	plt.legend(loc="upper right", bbox_to_anchor=(2.6,2.3), ncol=3, borderaxespad=0.)
else:
	region = results[ results.name.str.lower().str.startswith(sys.argv[1].lower()) ]
	pt = region.pivot_table(index='year', columns='abr',values='votes', fill_value=0)
	# line chart
	# if l > 2:
	# 	region.pivot_table(index='year', columns='abr',values='votes', fill_value=0)[sys.argv[2:]].plot(xticks=region.year.unique())
	# else:
	# 	region.pivot_table(index='year', columns='abr',values='votes', fill_value=0).plot(xticks=region.year.unique())

	if l > 2:
		#pt[sys.argv[2:]].plot(kind='barh', stacked=True)
		#pt.plot.barh(y=['INC','TDP','YSRCP','CPI'], stacked=True, color=['g','y','b','r'])
		C = [cm.Paired(partycolor[i]) for i in sys.argv[2:]]
		pt.plot.barh(y=sys.argv[2:], stacked=True, color=C)
	else:
		C = [cm.Paired(partycolor[i]) for i in pt.columns]
		pt.plot.barh(y=pt.columns, stacked=True, color=C)
		#pt.plot(kind='barh', stacked=True)

plt.show()