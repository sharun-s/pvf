# FULL MERGE steps

# #step 1 
# don't use output of extractTC
# instead import apur*-clean.csv files (cleaned in refine)
# and concat into m

# remove unnecessary columns

# add 'electedas' = "MPTC"
# remove whitespace, \n in name, mandal, set titlecase

# #step 2
# bossdf concat presidents p01, p06, p14
# check for and remove whitespace, \n in name, mandal  
# set titlecase

# reconcile mandal names between bossdf and m
# test - mandal count of concatented df should not be much more than  unique mandal count induvidual dfs 

# parties must match, year must match

# # p14 and mptc14 of 2014 must have matching mandals
# mismatches =  rlb.p14[rlb.p14['mandal'].isin(rlb.a[rlb.a['year']==2014].mandal)].shape
# 	- p14.shape[0]

# #p14[p14['president'].isin(a[rlb.a['year']==2014].name)]

# for i in rlb.p14.mandal:
#      i, showOptions(i, rlb.p14, rlb.mptc)

# def showOptions(mandal, bossdf, alldf):
# 	pm = bossdf[bossdf.mandal == mandal].president
# 	allm = alldf[alldf.mandal == mandal].name
# 	print(difflib.get_close_matches(pm, allm))

# setPresidents("Agali", rlb.p14, rlb.mptc)

# step 3: those that match set 'electedas' to MPTC PRESIDENT, MPTC VP, COPT MEMBER 

# step 4:
# check if year exists and 
# concat of mptc, mptc06, mptc14

# [c01, c06, c14]

# ================================
import difflib
import pandas as pd 

p01 = pd.read_csv('apur_mpPres_2001.csv')
p06 = pd.read_csv('apur_mpPres_2006.csv')
p14 = pd.read_csv('apur_mpPres_2014.csv')
m01=pd.read_csv("apur_mptc_2001-clean1.csv")
m06=pd.read_csv("apur_mptc_2006-clean1.csv")
m14=pd.read_csv("apur_mptc_2014-clean1.csv")

mv = pd.read_csv("mandal_spelling_variants.txt", names=['variant','standard'], index_col=0 )
def getSpellingVariants(mandal):
	if mandal in mv.index:
		tmp = mv.loc[mandal]
		if tmp.size ==1: 
			return [tmp.standard]
		else:
			return tmp.standard.values # return all variants
	else:
		return None 

data = [ (m01, p01), (m06, p06), (m14,p14)]

for i in data:
	i[0].drop(['president','pparty','vp','vpparty','cooptmember'],axis=1,inplace=True)
	i[0]['electedas']='MPTC'
tmp=None
def setPresidents(mandal, bossdf, alldf):
	pm = bossdf[bossdf.mandal == mandal].president
	allm = alldf[alldf.mandal == mandal]['name']
	if len(allm) == 0:
		print(mandal + " not found, checking with spelling variations...")
		v=getSpellingVariants(mandal)
		found=False
		for variant in v:
			if alldf[alldf.mandal == variant].shape[0] >0:
				allm = alldf[alldf.mandal == variant]['name']
				print(mandal+" not found, using variant ", variant)
				found=True
				break
		if not found:	
			print(mandal," not found")
			return
	j = allm[allm.isin(pm)].index
	if len(j)==1:
		print(pm.values[0], 'found in', mandal)
		#y=input(alldf.iloc[j[0]])
		#if y=='y':
		alldf.loc[j[0],'electedas']='MPTC President'
	elif len(j)>1: 
		print(mandal, "multiple found", j )
	else: 
		sim = difflib.get_close_matches(pm.values[0], allm)
		if len(sim) > 0:
			#print(pm.values[0],"similar to(choose index)?")
			#pick=input(sim)
			#if pick.isnumeric():
			#	j=allm[allm.str.contains(sim[int(pick)])].index
			#	print("setting electedas on ", j[0])
			#	alldf.loc[j[0],'electedas']='MPTC President'
			# TO RUN a manual check uncomment above comment below
			# WARNING: 1st match is auto selected in code below.  
			print(pm.values[0],'->',sim[0])
			j=allm[allm.str.contains(sim[0])].index
			#print("setting electedas on ", j[0])
			alldf.loc[j[0],'electedas']='MPTC President'
		else:
			largest = max(max(pm.values[0].split(' '), key=lambda x:len(x)).split('.'), key=lambda x:len(x))
			print('largest', largest)
			#global tmp
			#tmp = allm
			options = allm[allm.str.lower().str.contains(largest.lower())].values
			#print(pm.values[0], 'matches?') 
			#pick=input(options)
			#if pick.isnumeric():
			if len(options)>0:
				#j=allm[allm.str.contains(options[int(pick)])].index
				print(pm.values[0],'>>',options[0])
				j=allm[allm.str.contains(options[0])].index
				#print("setting electedas on ", j[0])
				alldf.loc[j[0],'electedas']='MPTC President'
			else:
				print('mandal pres not set for ', mandal) 

def setVPs(mandal, bossdf, alldf):
	pm = bossdf[bossdf.mandal == mandal].vp
	allm = alldf[alldf.mandal == mandal]['name']
	if len(allm) == 0:
		print(mandal + " not found, checking with spelling variations...")
		v=getSpellingVariants(mandal)
		found=False
		for variant in v:
			if alldf[alldf.mandal == variant].shape[0] >0:
				allm = alldf[alldf.mandal == variant]['name']
				print(mandal+" not found, using variant ", variant)
				found=True
				break
		if not found:	
			print(mandal," not found")
			return
	j = allm[allm.isin(pm)].index
	if len(j)==1:
		print(pm.values[0], 'found in', mandal)
		alldf.loc[j[0],'electedas']='MPTC Vice President'
	elif len(j)>1: 
		print(mandal, "multiple found", j )
	else: 
		sim = difflib.get_close_matches(pm.values[0], allm)
		if len(sim) > 0:
			print(pm.values[0],'->',sim[0])
			j=allm[allm.str.contains(sim[0])].index
			alldf.loc[j[0],'electedas']='MPTC Vice President'
		else:
			largest = max(max(pm.values[0].split(' '), key=lambda x:len(x)).split('.'), key=lambda x:len(x))
			print('largest', largest)
			options = allm[allm.str.lower().str.contains(largest.lower())].values
			if len(options)>0:
				print(pm.values[0],'>>',options[0])
				j=allm[allm.str.contains(options[0])].index
				alldf.loc[j[0],'electedas']='MPTC Vice President'
			else:
				print('mandal pres not set for ', mandal) 


def reconcile(data):
	for a, b in data:
		for i in b.mandal:
			setPresidents(i, b, a)

def countUpdated(data):
	for a,b in data:
		print(a['electedas'].value_counts()['MPTC President'],'/',b.shape[0],'/',a.shape[0])

def notSet(data):
	for a,b in data:
		print(a[~a.mandal.isin(a[a.electedas == "MPTC President"].mandal)].mandal.unique())

def manualSet(df, index, val):
	df.loc[index, 'electedas']=val # eg 'MPTC President'

#debugging helper fns
g=lambda x,y:x[x.mandal == y]
gco=lambda x,y:x[x.mandal.str.contains(y)]

reconcile(data)
countUpdated(data)
for i in p14.mandal:
	setVPs(i, p14, m14)

# manual fix
def Hack():
	manualSet(m06, 135, "MPTC President")
	manualSet(m06, 445, "MPTC President")
	manualSet(m06, 673, "MPTC President")
	manualSet(m14, 167, "MPTC President")
	manualSet(m14, 297, "MPTC Vice President")
	manualSet(m14, 46, "MPTC Vice President")

notSet(data)

# VP's not set
m14[~m14.mandal.isin(m14[m14.electedas == "MPTC Vice President"].mandal)].mandal.unique()
# VP's set
m14['electedas'].value_counts()['MPTC Vice President'],'/',p14.shape[0]

m=pd.concat([m01, m06, m14], ignore_index=True)
m.to_csv("apur_mandal_parishad_history.csv", index=False)

#vc = m.name.value_counts()
#vc[vc > 1] # 89/2216