import sys, difflib
import pandas as p

df=[]
for i in sys.argv[2:]:
	df.append(p.read_csv(i))

districtfilter = lambda x: x.mandal.str.startswith(sys.argv[1])

mandals_year = []
for i in df:
	mandals_year.append(i[districtfilter(i)].area.sort_values().to_list())

for i in range(0,len(mandals_year)-1):
	noc, splitm, delm, newm=[],[],[],[]
	a = set(mandals_year[i])
	b = set(mandals_year[i+1])
	noc = a.intersection(b)
	allsimilar = []
	for j in a.difference(b):
	     similar = difflib.get_close_matches(j, b)
	     if len(similar) == 0:
	     	delm.append(j)
	     else:
	     	splitm.append((j,similar))
	     	allsimilar.extend(similar)
	newm=b.difference(a).difference(allsimilar)
	print('no change', len(noc), noc)
	print()
	print('removed', len(delm), delm)
	print()
	print('added', len(newm), newm)
	print()
	print('division or mistakes', len(splitm), splitm )