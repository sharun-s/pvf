import simplejson
import sys
f=open(sys.argv[1], 'r')
zj=simplejson.load(f)
for i in zj:
	if 'edits' in i:
		print(','.join([i['edits'][0]['from'][0],i['edits'][0]['to']]))
f.close()