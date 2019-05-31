import camelot
from pprint import pprint
import pandas as pd

tables = camelot.read_pdf(r'../pdfs-apec/2014/List of Elected Mayors, 2014 (Andhra).pdf')
d=tables[0].df
# use iloc to access the row and df[colindex] to access col
# replace whitespace newlines etc with single space
removews = lambda x: ' '.join(x.split()).title()
mayor_apur_2014 = removews(d.iloc[6][4]) , d.iloc[6][3], d.iloc[6][5] 
dmayor_apur_2014 = removews(d.iloc[6][6]) , d.iloc[6][3] ,d.iloc[6][7]
ppl=[{'year':2014, 'name':'Madamanchi Swaroopa', 'party':'TDP', 'sex':'F', 'electedas':'Mayor', 'electioncat':d.iloc[6][3], 'area':'Anantapur MuniCorp'}, 
{'year':2014, 'name':'Sake Gampanna', 'party':'TDP', 'sex':'M', 'electedas':'Deputy Mayor', 'area':'Anantapur MuniCorp', 'electioncat':d.iloc[6][3]}]
munitables = camelot.read_pdf(r'../pdfs-apec/2014/Anantapur-Municipalities-Chairpersons-2014.pdf', pages='2-end')
r1=[]
for i in range(0,len(munitables)):
	mdf=munitables[i].df
	r1.append(mdf[mdf[1]=='Anantapur'])

# so first read pdf and generate tables per page. this can be filtered by column eg mdf[1]=='Ananta..'none 
# empty dataframes have to be appended. then iterate over the results and 
# extract fields colmn wise using iloc appending entries to ppl. 2 passes cause one pass extract chair other extracts deputy. Sex and spellings and whitespace in names have to be manually handled
#readline.write_history_file(r'/home/s/apur/pdf2tables.log')
r=r1[2].append(r1[3])
for i in range(0, r.shape[0]):
	ppl.append({'name':removews(r.iloc[i][6]), 'party':r.iloc[i][7], 'sex':'F' if r.iloc[i][3].find('omen')>-1 else 'M?' , 'electedas':'MuniViceChairman', 'year':2014, 'area':r.iloc[i][2]+' Muni', 'electioncat':r.iloc[i][3]})
for i in range(0, r.shape[0]):
	ppl.append({'name':removews(r.iloc[i][4]), 'party':r.iloc[i][5], 'sex':'F' if r.iloc[i][3].find('omen')>-1 else 'M?' , 'electedas':'MuniChairman', 'year':2014, 'area':r.iloc[i][2]+' Muni', 'electioncat':r.iloc[i][3]})

#Mayor + Deputy Mayor + Corporators - Anantapur MuniCorp
#List of Elected Mayors, 2014 (Andhra).pdf
#Andhra Elected Corporators List, 2014.pdf
#Chairman + ViceChairman + Councillors - all municipalities (11)
#Anantapur-Municipalities-Chairpersons-2014.pdf
#Andhra Elected councilors List, 2014.pdf

# Munical Councilors - 11 Municipalities - 323 wards
municouncilors = camelot.read_pdf(r'../pdfs-apec/2014/Andhra Elected councilors List, 2014.pdf', pages='1-8')

d=pd.DataFrame()
for i in range(0, len(municouncilors)):
  cdf=municouncilors[i].df
  tmp=cdf[cdf[1]=='Anantapur']
  if len(tmp) != 0:
    if d.empty:
      d = tmp
    else:
      d=d.append(tmp)

for i in range(0, d.shape[0]):
  ppl.append({'name':removews(d.iloc[i][5]), 'party':d.iloc[i][6], 'sex':'F' if d.iloc[i][4].find('(W)')>-1 else 'M?' , 'electedas':'MuniCouncilor', 'year':2014, 'area':d.iloc[i][2]+' Muni','ward':d.iloc[i][3], 'electioncat':d.iloc[i][4]})

# Municipal Corporators - 1 MuniCorp - 50?wards
municorporators = camelot.read_pdf(r'../pdfs-apec/2014/Andhra Elected Corporators List, 2014.pdf', pages='8-9')
d=pd.DataFrame()
for i in range(0, len(municorporators)):
  cdf=municorporators[i].df
  tmp=cdf[(cdf[1]=='') | (cdf[1] =='Anantapur')]
  if len(tmp) != 0:
    if d.empty:
      d = tmp
    else:
      d=d.append(tmp)

for i in range(0, d.shape[0]):
  ppl.append({'year':2014, 'name':removews(d.iloc[i][4]), 'party':d.iloc[i][5], 'sex':'F' if d.iloc[i][3].find('(W)')>-1 else 'M?', 
    'electedas':'MuniCorporator', 'area':'Anantapur MuniCorp',
    'ward':d.iloc[i][2], 'electioncat':d.iloc[i][3]})

#ulb = pd.DataFrame(ppl, columns=ppl[0].keys())
ulb = pd.DataFrame(ppl)

# Municipal Results 2014 also shows losing contestants/party and vote count per ward in municorp and muni

