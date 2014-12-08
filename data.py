import urllib, json
offset = 0
f = open('data/games.json','a')
while offset<3495:
	
	url = "https://www.giantbomb.com/api/releases/?api_key=7e672687f183619ce64402ae075d3c63173c5c5e&format=json&offset="+str(offset)+"field_list=name,release_date,genre,platform&filter=release_date:2014-01-01%2000:00:00|2014-12-31%2000:00:00"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	json.dump(data,f)
	offset+=100
