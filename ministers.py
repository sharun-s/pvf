import pandas as pd
from os import listdir
import difflib

repdb=pd.read_csv("data/rep.csv")

l=[fn for fn in listdir('data/') if fn.startswith("ap_ministers")]
years=[{"file":i,"year":int(i[:-4].split("_")[2]),"key":"_".join(i[:-4].split("_")[2:])} for i in l]
years.sort(key=lambda x:x["year"])

for i in years:
	ministers_thatyear=pd.read_csv("data/"+i["file"], header=None, comment='#', names=['minister'],usecols=[0])
	#print(ministers_that_year)
	mlas_thatyear = repdb[(repdb.year==i["year"]) & (repdb.electedas=="MLA")].name
	print(i['year'],i['file'])
	#print(mlas_thatyear)
	from_apur= mlas_thatyear[mlas_thatyear.isin(ministers_thatyear["minister"])].index
	if len(from_apur) >0:
		print("**found",from_apur)
		repdb.loc[from_apur,"electedas"]="MLA Minister"
		print(repdb.loc[from_apur])
	# for i in mlas_thatyear:
	# 	#print(type(i),type(mlas_thatyear.values))
	# 	sim = difflib.get_close_matches(i, ministers_that_year.minister.values)
	# 	if len(sim)>0:
	# 		print('difflib',i,sim)
	# for i in mlas_thatyear:
	# 	largest = max(max(i.split(' '), key=lambda x:len(x)).split('.'), key=lambda x:len(x))
	# 	#print(largest)
	# 	sim = difflib.get_close_matches(largest, ministers_that_year.minister.values)
	# 	if len(sim)>0:
	# 		print('largestsub',i,sim)
	
repdb.to_csv("data/rep.csv",index=False)
