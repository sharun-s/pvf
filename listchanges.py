import simplejson
import sys
f=open(sys.argv[1], 'r')
zj=simplejson.load(f)
colname='mandal'
if len(sys.argv) == 3:
  colname = sys.argv[2]

for i in zj:
	if 'edits' in i and colname == i['columnName']:
		print(','.join([i['edits'][0]['from'][0],i['edits'][0]['to']]))

	if 'expression' in i:
		if i['expression'] != 'value':
			print (i['columnName']+' '+i['expression'])

f.close()