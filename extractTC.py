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

# 2001 Mandal Parishad Presidents
pres01_tables=camelot.read_pdf(r'../pdfs-apec/2001/MP Presidents 2001.pdf', flavor='stream', pages='1-2')
p01 = pres01_tables[0].df
p02 = pres01_tables[1].df
p01 = p01[2:]
p02 = p02[2:]
p01=p01.append(p02, ignore_index=True)
k=p01[p01[0]!=''].index
p01=p01.iloc[k[1]:k[2]]
p01['electioncat'], p01['name'] = p01[2].str.split('\n').str
p01=p01.drop(2, axis=1)
p01=p01.drop(0, axis=1)
p01.columns=['mandal', 'party', 'electioncat', 'name']
p01.party.value_counts()         

# 2006 Mandal Parishar Presidents
pres06_tables=camelot.read_pdf(r'../pdfs-apec/2006/MP Presidents 2006.pdf', flavor='stream', pages='2-3')
p06= pres06_tables[0].df
p061= pres06_tables[1].df
p06=p06[3:]
p06=p06.append(p061[3:], ignore_index=True)
k=p06[p06[0]!=''].index
p06=p06.iloc[k[0]:k[1]]
p06=p06.drop(0, axis=1)
p06.columns=['mandal', 'name', 'party']

#2014 Mandal Parishad Presidents
pres14_tables=camelot.read_pdf(r'../pdfs-apec/2014/Anantapur-MPP-2014.pdf', pages='1-4')
p14= pres14_tables[0].df
p14=p14[2:]
for i in range(0,len(pres14_tables)):
  p14=p14.append(pres14_tables[i].df[2:], ignore_index=True)
 
k=p14[p14[1]!=''].index
p14=p14.iloc[k[1]:k[2]]
p14=p14.drop(0, axis=1)
p14=p14.drop(1, axis=1)
p14.columns=['mandal','electioncat', 'president', 'pparty', 'vp', 'vpparty', 'cooptmember']

# p01[p01.mandal == 'Agali'].name
# p06[p06.mandal == 'Agali'].name
# p14[p14.mandal == 'Agali'].president
# mptc01[mptc01.mandal == 'Agali']
# mptc06[mptc06.mandal == 'Agali']
# mptc14[mptc14.mandal == 'Agali']

#Chairman & Vice-Chairman Zila Parishad 2001
chair01_tables=camelot.read_pdf(r'../pdfs-apec/2001/Chairman list 2001.pdf', flavor='stream')
c01 = chair01_tables[0].df
c01 = c01[c01[1].str.contains('Anan')]
c01 = c01.drop([0, 1], axis=1)
c01.columns = ['electioncat', 'chair', 'chairparty', 'vicechair', 'vcparty']
print(c01.chair)

#Chairman & Vice-Chairman Zila Parishad 2006
zp14[zp14.name.str.contains(c14.chair.values[0])]
chair06_tables=camelot.read_pdf(r'../pdfs-apec/2006/Chairman & Vice-Chairman list 2006.pdf')
>>> c06 = chair06_tables[0].df
c06[c06[1].str.contains('Anan')]
#UR(W)  T Kavithamma  INC  Muddala Narsimhulu  INC  1. Khaja Moinuddin  2. S Jaffer vali
c06 = c06[c06[1].str.contains('Anan')]
c06 = c06.drop(0, axis=1)
c06 = c06.drop(1, axis=1)
c06.columns = ['electioncat', 'chair', 'chairparty', 'vicechair', 'vcparty', 'coptmember1', 'coptmember2']
# c06.chair.values[0]
# 'T Kavithamma'
# >>> zp06[zp06.name.str.contains('Kavi')]
# 12  Rapthadu  T.Kavithamma   INC       UR(W)      Kapu  M.A.  42   F
# >>> zp06[zp06.name.str.contains('Mudda')]
#   Nallamada   Muddala Narasimhulu   INC          BC      Boya  HSLC  54   M

#Chairman & Vice-Chairman Zila Parishad 2014
chair14_tables=camelot.read_pdf(r'../pdfs-apec/2014/Anantapur-ZPP-2014.pdf')
c14 = chair14_tables[0].df
c14 = c14[c14[1].str.contains('Anan')]
c14 = c14.drop([0,1], axis=1)
#BC  D.Chaman Sab  TDP  Madineni.Subhashini  TDP  C.S.Abdul Ravoof  C.H.Jafroolla \nKhan
c14.columns = ['electioncat', 'chair', 'chairparty', 'vicechair', 'vcparty', 'coptmember1', 'coptmember2']
# zp14[zp14.name.str.contains('Chaman')]
# 46  Ramagiri          UR  D.Chaman Sab   TDP
# zp14[zp14.name.str.contains('Subha')]
# 7  Beluguppa       UR(W)  Madineni Subhasini   TDP
# zp14[zp14.name.str.contains(c14.chair.values[0])]
#       mandal electioncat          name party
# 46  Ramagiri          UR  D.Chaman Sab   TDP