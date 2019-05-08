import camelot
from pprint import pprint
import pandas as pd
removews = lambda x: ' '.join(x.split()).title()
ppl=[]
mptc_tables=camelot.read_pdf(r'../pdfs-apec/2014/Andhra Elected MPTCs List, 2014.pdf',pages='1-21')
dname = 'Ananthapur'
for i in range(0, len(mptc_tables)):
  d=mptc_tables[i].df
  isSubTotalRow = lambda row: d.iloc[row][2].isdigit()
  lastrow = d.shape[0]
  if d.iloc[1][0] == dname:
    mandal_indexlist = d.index[d[1]!=''].to_list()
    #print(mandal_indexlist)
    # if first index is 0
    #   if start row
    #     no issues 
    #   if stop row
    #     increment 1 
    # else if not 0
    #   if stop row
    #     inject 0 to beg of mandal_indexlist - 
    #   else
    #     bug - not possible

    # is last index stop row
    #   don't append endcount
    # else 
    #   append endcount 
    #if first row is a stop row pop it
    if isSubTotalRow(mandal_indexlist[0]):
      mandal_indexlist.pop(0)
    #else:
    #  mandal_indexlist.pop(0, 1)
    
    if not isSubTotalRow(mandal_indexlist[-1]):
      #mandal_indexlist[-1] = mandal_indexlist[-1] - 1 
    #else:
      mandal_indexlist.append(lastrow)
    #print(mandal_indexlist)
    for j in range(0, len(mandal_indexlist), 2):
      s = mandal_indexlist[j]
      e = mandal_indexlist[j+1]
      mandal = d.iloc[s][1]
      tmp= d[s:e] 
      # recheck district name is same or empty
      if tmp.iloc[0][0] == '' or tmp.iloc[0][0] == dname:
        for k in range(0, tmp.shape[0]): 
          if tmp.iloc[k][4]=='': # bug col 3 4 5 are being concatnated
            cols = tmp.iloc[k][3].split('\n')
            if len(cols) == 3:
              electioncat = cols[0]
              name = cols[1]
              party = cols[2]
            elif len(cols) == 4: #large names sometimes have \n in them
              electioncat = cols[0]
              name = cols[1]+' '+cols[3]
              party = cols[2]
            else:
              print(cols)
              print(tmp.iloc[k][3])
              name = party = electioncat = ''
              print('error')
              pprint(tmp)
          else:
            electioncat = tmp.iloc[k][3]
            name = removews(tmp.iloc[k][4])
            party = tmp.iloc[k][5]

          ppl.append({
              'mandal':mandal, 
              'area':tmp.iloc[k][2],
              'name': name, 
              'party': party, 
              'sex':'F' if electioncat.find('(W)')>-1 else 'M?',  
              'electioncat':electioncat,
              'year':'2014'})
#s=pd.Series(p['mandal'] for p in ppl)
#pprint(s.value_counts())
#print(len(set(s.values)))

#pprint(pdf)
mptc = pd.DataFrame(ppl, columns=ppl[0].keys())
mptc.area = mptc.area.str.title() # some are all caps
# write to disk
# mptc.to_csv(r'apur_mptc_2014.csv', index=False)

#print(mptc.groupby('mandal').size())
#mptc[mptc['mandal']=='Kanaganapalli']
#print(mptc['name'].count())

#print(mptc.groupby(['mandal', 'party']).size())
#geocode mandals
#import subprocess
#for n,g in pdf.groupby('mandal'):
#  o = subprocess.getoutput("./pvf/geocode.sh "+ n)
#  print(n, o)

#to find tot of each mandal
mptc.groupby('mandal').area.nunique()
#to find list of areas in each mandal
#pdf.groupby('mandal').area.unique()

# note shift_text=[''] makes sure values in a cell without boundaries arent move left or up which is the default
mptc06_tables=camelot.read_pdf('../pdfs-apec/2006/Anantapur_MPTC-2006.pdf', shift_text='', strip_text='\n', pages='1-end')

def prep(i):
  d = mptc06_tables[i].df
  # drop the first column S.No its not reqd
  d=d.drop(0, axis=1)
  d=d.drop(1, axis=1) # all rows have same value = districtname
  # rename col names - by default will be 1,2,3 etc
  d.columns = ['mandal', 'area', 'name', 'party', 'electioncat', 'community', 'edu', 'age', 'sex', 'occupation']
  # drop header row
  return d[1:]

mptc06=prep(0)
for i in range(1, len(mptc06_tables)):
  mptc06=mptc06.append(prep(i), ignore_index=True) 

#import matplotlib.pyplot as pyplot
#d.groupby([age']).size().plot('bar')
#plt.show()

# 2001 MPTC
mptc01_tables=camelot.read_pdf(r'../pdfs-apec/2001/Anatapur-MPTC-2001.pdf', flavor='stream', pages='9-21')
# since there are blank spaces and cell values have to be filled
# from prev row where value exists just like in 2014 table district column 
# ideally camelot readpdf with copy_text would handle this but doesnt work with stream
def prep01(i):
  d = mptc01_tables[i].df
  # drop the first column S.No its not reqd
  #d=d.drop(0, axis=1)
  #d=d.drop(1, axis=1) # all rows have same value = districtname
  # rename col names - by default will be 1,2,3 etc
  d.columns = ['district', 'mandal', 'area', 'name', 'party']
  # drop title row + header row
  return d[2:]

mptc01=prep01(0)
for i in range(1, len(mptc01_tables)):
  mptc01=mptc01.append(prep01(i), ignore_index=True)

#only pull out rows corresponding to the district
k=mptc01[mptc01['district']!=''].index
# this gives the index boundaries for one district
mptc01=mptc01.iloc[k[0]:k[1]]
#now district name col can be dropped as it can only be the same thing
mptc01=mptc01.drop('district', axis=1)
# since mandal name is only present in first row all following rows need to be foward filled with that name
mptc01.mandal.fillna(method='ffill')
mptc01.mandal = mptc01.mandal.replace('', None)

mptc06['year'] = 2006
mptc01['year'] = 2001
mptc['year']=2014
a=pd.concat([mptc, mptc06, mptc01], axis=0, ignore_index=True)
#a.party.value_counts()

zptc01_tables=camelot.read_pdf(r'../pdfs-apec/2001/Anantapur-ZP-2001.pdf', flavor='stream', pages='2-3')
def prep02(i):
  d = zptc01_tables[i].df
  d.columns = ['district', 'mandal', 'name', 'party', 'electioncat']
  # drop title row + header row
  return d[2:]
zp01=prep02(0)
# since only two pages no need for loop
zp01=zp01.append(prep02(1), ignore_index=True)
k=zp01[zp01['district']!=''].index
zp01=zp01.iloc[k[0]:k[1]]
#now district name col can be dropped as it can only be the same thing
zp01=zp01.drop('district', axis=1)

# shift_text='' is not enough - long names with \n get pushed down to next cell
zptc06_tables=camelot.read_pdf(r'../pdfs-apec/2006/anantapur-ZP-2006.pdf', pages='1-end')
def prep03(i):
  d = zptc06_tables[i].df
  d=d.drop(0, axis=1) # drop s.no not reqd
  d=d.drop(9, axis=1) # drop occupation - col isempty
  d.columns = ['mandal', 'name', 'party', 'electioncat', 'community', 'edu', 'age' , 'sex']
  # drop title row + header row
  d.mandal = d.mandal.str.title()
  return d[2:]
zp06=prep03(0)
for i in range(1,len(zptc06_tables)):
  zp06=zp06.append(prep03(i), ignore_index=True)

mistakes = zp06[zp06.mandal.str.contains('\n')].index
print('mistakes',len(mistakes))
for i in mistakes:
  tokens = zp06.iloc[i]['mandal'].split('\n') 
  zp06.iloc[i-1]['mandal']= zp06.iloc[i-1]['mandal'] +' '+ tokens[0]  
  zp06.iloc[i]['mandal']= ' '.join(tokens[1:])  
 
mistakes = zp06[zp06.mandal.str.contains('\n')].index
print('mistakes',len(mistakes)) # should be zero

mistakes = zp06[zp06.name.str.contains('\n')].index
print('mistakes',len(mistakes))
for i in mistakes:
  tokens = zp06.iloc[i]['name'].split('\n') 
  zp06.iloc[i-1]['name']= zp06.iloc[i-1]['name'] +' '+ tokens[0]  
  zp06.iloc[i]['name']= ' '.join(tokens[1:])  
 
mistakes = zp06[zp06.name.str.contains('\n')].index
print('mistakes',len(mistakes))

#zp06.age.value_counts().sort_index().plot('bar')
#zp06.age.astype(int).value_counts(bins=[0, 20, 30, 40, 50, 60, 100]).sort_index().plot('pie')
#plt.show()

zptc14_tables=camelot.read_pdf(r'../pdfs-apec/2014/Andhra Elected ZPTCs List, 2014.pdf', pages='1-2', copy_text=['v'])
def prep04(i):
  d = zptc14_tables[i].df
  d.columns = ['district', 'mandal', 'electioncat', 'name', 'party']
  return d[1:]
zp14=prep04(0)
# only 2 pages so no need for loop
zp14=zp14.append(prep04(1), ignore_index=True)
k=zp14[zp14['district']!=''].index
zp14=zp14.iloc[k[0]:k[2]] # here format is again diff from above 2 distname occurs at begining of each page and as subtot
#now district name col can be dropped as it can only be the same thing
zp14=zp14.drop('district', axis=1)

print(zp01.party.value_counts())
print(zp06.party.value_counts())
print(zp14.party.value_counts())
