import matplotlib.pyplot as plt
import sys
import pandas as p
#from optparse import OptionParse
#parser = OptionParser()
#parser.add_option()

# arg1 - region name or partial segment name
# arg2 - party abr eg TDP INC CPI will draw just those 3, if none show all

l = len(sys.argv)

results = p.read_csv("apur.tsv", delimiter='\t')

region = results[ results.name.str.lower().str.startswith(sys.argv[1].lower()) ]

if l > 2:
	region.pivot_table(index='year', columns='abr',values='votes', fill_value=0)[sys.argv[2:]].plot(xticks=region.year.unique())
else:
	region.pivot_table(index='year', columns='abr',values='votes', fill_value=0).plot(kind='barh', xticks=region.year.unique())

plt.show()