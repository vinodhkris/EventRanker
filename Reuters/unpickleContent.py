import test
import sys

if len(sys.argv)>1:
	smDict = test.unpickle(sys.argv[1])
else:
	sys.exit(0)

for i in xrange(len(smDict)):
	try:
		print i,smDict[i]["web_url"],smDict[i]["headline"],smDict[i]["pub_date"]
	except:
		continue
