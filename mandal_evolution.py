import sys, difflib
import pandas as p
# arg1 - mandal name or partial mandal name
# arg2 - numeric print numeric summary without shell colors
#		 v -  verbose output
#		 else print numeric summary with shell colors
# arg3 - list of files that need to be compared eg year1.csv year2.csv year3.csv

df=[]
for i in sys.argv[3:]:
	df.append(p.read_csv(i))

mandalfilter = lambda x: x.mandal.str.lower().str.startswith(sys.argv[1].lower())

mandal_name = df[0][mandalfilter(df[0])].mandal.unique()[0]
mandals_year = []
for i in df:
	areas = i[mandalfilter(i)].area.str.title().sort_values().to_list()
	mandals_year.append(areas)

if sys.argv[2].isdigit():
	tmp=mandal_name+" " + str(len(mandals_year[0]))
else:
	tmp=mandal_name+" \033[1;32;60m"+str(len(mandals_year[0]))

for i in range(0, len(mandals_year)-1):
	if len(mandals_year[i]) <= len(mandals_year[i+1]):
		if sys.argv[2].isdigit():
			tmp = tmp+" "+str(len(mandals_year[i+1]))
		else:
			tmp = tmp+"\x1b[1;32;60m->"+str(len(mandals_year[i+1]))
	else:
		if sys.argv[2].isdigit():
			tmp = tmp+" "+str(len(mandals_year[i+1]))
		else:
			tmp = tmp+"\x1b[1;31;60m->"+str(len(mandals_year[i+1]))

if sys.argv[2].isdigit():
	print(tmp)
else:
	print(tmp+"\033[0m")


for i in range(0,len(mandals_year)-1):
	noc, splitm, delm, newm=[],[],[],[]
	a = set(mandals_year[i])
	b = set(mandals_year[i+1])
	noc = a.intersection(b)
	allsimilar = []
	for j in a.difference(b):
		#print(j, b) # BUG if b contains nan, emptyspace
		similar = difflib.get_close_matches(j, b)
		if len(similar) == 0:
			delm.append(j)
		else:
			splitm.append((j,similar))
			allsimilar.extend(similar)
	newm=b.difference(a).difference(allsimilar)
	if sys.argv[2].isdigit():
		tmp='' #noop 
	elif sys.argv[2] == 'v':
		print('=' + str(len(noc)), '\x1b[1;31;60m-'+str(len(delm)),
		'\x1b[0m\x1b[1;32;60m+'+ str(len(newm)),
		'\x1b[0m\x1b[1;36;60m?'+ str(len(splitm))+'\x1b[0m')
	else:
		print('no change', len(noc), noc)
		print()
		print('removed', len(delm), delm)
		print()
		print('added', len(newm), newm)
		print()
		print('division or mistakes', len(splitm), splitm )