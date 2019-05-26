import csv, json
import requests

def getresults(asscode):
	r=requests.get("https://election.nw18.com/electiondata/electionjson/general_election_2019/live/assembly/constituency/"+asscode+".json?jsonp=election_const")
	results = json.loads(r.content[15:-1])
	for i in results['data']:
		apur2019.append([2019,'MLA',i['CNAME'],i['CCODE'],i['PCODE'], i['CANDINAME'], i['ABBR'], i['VOTES'], i['VALID_VOTES'],i['voting_percentage']])

apur2019 = []
getresults('s01a153')
getresults('s01a154')
getresults('s01a152')
getresults('s01a151')
getresults('s01a150')
getresults('s01a149')
getresults('s01a148')

f=open('apur2019assembly.csv',"w")
w = csv.writer(f)
w.writerows(apur2019)
f.close()	

a2019 = p.read_csv("apur2019assembly.csv", header=None)
a2019.columns = ["year", "electedas", "name", "code", "pcode", "cname", "abr", "votes", "tot", "perc"]
b=p.concat([a, a2019], ignore_index=True, join="inner")	
b.to_csv(r'apur.csv', index=False)