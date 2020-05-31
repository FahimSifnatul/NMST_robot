import json
import requests as req
import wikipediaapi

q = "werqwerewwrwrwerweasdasdfewrerwrwrwerfasdfdsfaf"
url = "https://app.zenserp.com/api/v2/search?apikey=3006e4b0-5578-11ea-8b01-070206ede933&q=" + q
try:
	ret = req.get(url)
	#print(ret.text)
	json_data = json.loads(ret.text)
	#print(json_data)
	
	res = json_data["organic"]
	#print(len(res))
	for i in range(10):
		title = res[i]["title"]
		title_parts = [x for x in title.split()]
		if 'Wikipedia' in title_parts:
			#print(res[i]["description"])
			wiki = wikipediaapi.Wikipedia('en')
			
			wiki_title = title.split(' - ')[0]
			print(wiki_title)
			wiki_res = wiki.page(wiki_title)
			
			wiki_len = min(1000, len(wiki_res.summary))
			print("Page - Summary: %s" % wiki_res.summary[0:wiki_len])
			break
except:
	print("no answer or offline.")


