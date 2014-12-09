import urllib, json, unirest, datetime, calendar
def convertToDateTime(date_str):
	#2014-10-16 00:00:00
	year=date_str[0:4]
	month = date_str[5:7]
	day = date_str[8:10]
	print date_str
	return datetime.datetime(int(year), int(month), int(day), 0, 0)

def monthStr(month_int):
	month = int(month_int)
	if(month==1):
		return "January"
	elif(month==2):
		return "February"
	elif(month==3):
		return "March"
	elif(month==4):
		return "April"
	elif(month==5):
		return "May"
	elif(month==6):
		return "June"
	elif(month==7):
		return "July"
	elif(month==8):
		return "August"
	elif(month==9):
		return "September"
	elif(month==10):
		return "October"
	elif(month==11):
		return "November"
	elif(month==12):
		return "December"
offset = 0
f = open('data/games.json','w')
f2 = open('data/datas.json', 'w')
gameResults=[]
timeResults={}
noneCount = 0
platformSet = set([])
uniqueGameNames = set([])
#3495 for 2014
while offset<2000:
	
	url = "https://www.giantbomb.com/api/releases/?api_key=7e672687f183619ce64402ae075d3c63173c5c5e&format=json&offset="+str(offset)+"&field_list=name,release_date,site_detail_url,genre,platform&filter=release_date:2014-01-01%2000:00:00|2014-12-31%2000:00:00"
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	i = 0
	resultSize = len(data["results"])
	while (i < resultSize):
		if(data["results"][i]["release_date"] != None):
			# "1": "PlayStation 3",
			#     "2": "Xbox 360",
			#     "3": "PC",
			#     "4": "DS",
			#     "6": "PlayStation 2",
			#     "7": "PSP",
			#     "8": "Wii",
			#     "9": "iPhone/iPad",
			#     "10": "PlayStation",
			#     "11": "Game Boy Advance",
			#     "12": "Xbox",
			#     "13": "GameCube",
			#     "14": "Nintendo 64",
			#     "15": "Dreamcast",
			#     "16": "3DS",
			#     "67365": "PlayStation Vita",
			#     "68410": "Wii U",
			#     "72496": "PlayStation 4",
			#     "80000": "Xbox One"
			mcPlat= 0
			platform = data["results"][i]["platform"]["name"]
			gameName = data["results"][i]["name"]+"."+platform
			platformSet.add(platform)
			if(platform=="PlayStation 3" or platform=="PlayStation Network (PS3)"):
				mcPlat = 1
			elif(platform=="Xbox 360" or platform=="Xbox 360 Games Store"):
				mcPlat = 2
			elif(platform=="PC" or platform=="Linux" or platform=="Mac"):
				mcPlat = 3
			elif(platform=="Nintendo DS" or platform =="DSiWare"):
				mcPlat = 4
			elif(platform=="PlayStation 2"):
				mcPlat = 6
			elif(platform=="PlayStation Portable" or platform=="PlayStation Network (PSP)"):
				mcPlat = 7
			elif(platform=="Wii" or platform=="Wii Shop"):
				mcPlat = 8
			elif(platform=="iPhone" or platform=="IPad"):
				mcPlat = 9
			elif(platform=="PlayStation"):
				mcPlat = 10
			elif(platform=="PlayStation Vita" or platform=="PlayStation Network (Vita)"):
				mcPlat = 67365
			elif(platform=="Wii U"):
				mcPlat = 68410
			elif(platform=="Nintendo 3DS" or platform=="Nintendo 3DS eShop"):
				mcPlat = 16
			elif(platform=="PlayStation 4"):
				mcPlat = 72496
			elif(platform=="Xbox One"):
				mcPlat = 80000
			elif(platform=="GameCube"):
				mcPlat = 13
			elif(platform=="Dreamcast"):
				mcPlat = 15

			# These code snippets use an open-source library. http://unirest.io/python
			if(mcPlat!=0):
				mcResponse = unirest.post("https://byroredux-metacritic.p.mashape.com/search/game",
				  headers={
				    "X-Mashape-Key": "EH1nc2m4yDmshwgsHTweFUIFxXaJp1eJsYgjsnfs4eKkDP7LQy",
				    "Content-Type": "application/x-www-form-urlencoded"
				  },
				  params={
				    "max_pages": 1,
				    "platform": mcPlat,
				    "retry": 4,
				    "title": data["results"][i]["name"]
				  }
				)
				print platform

				#nothing was found within this query, retry with no specific platform
				if not mcResponse.body.get('code'):
					if(mcResponse.body['count'] == 0):
						mcResponse2 = unirest.post("https://byroredux-metacritic.p.mashape.com/search/game",
						  headers={
						    "X-Mashape-Key": "EH1nc2m4yDmshwgsHTweFUIFxXaJp1eJsYgjsnfs4eKkDP7LQy",
						    "Content-Type": "application/x-www-form-urlencoded"
						  },
						  params={
						    "max_pages": 1,
						    "retry": 4,
						    "title": data["results"][i]["name"]
						  }
						)
						if(mcResponse2.body['count']!=0):
							score= mcResponse2.body["results"][0]['score']
							data["results"][i]["score"] = score
							data["results"][i]["release_month"] = monthStr(data["results"][i]["release_date"][5:7])
							data["results"][i]["name"] = gameName
							data["results"][i]["url"] = data["results"][i]["site_detail_url"]
							if(score!="" and (gameName not in uniqueGameNames)):

								release = data["results"][i]["release_date"]
								epoch = calendar.timegm(convertToDateTime(release).timetuple())
								timeResults[str(epoch)]=int(score)
								gameResults.append(data["results"][i])
							#otherwise, don't log it into the database, it is scoreless
					else:
						score= mcResponse.body["results"][0]["score"]
						data["results"][i]["score"] = score
						data["results"][i]["release_month"] = monthStr(data["results"][i]["release_date"][5:7])
						data["results"][i]["name"] = gameName
						data["results"][i]["url"] = data["results"][i]["site_detail_url"]
						if(score!="" and (gameName not in uniqueGameNames)):
							release = data["results"][i]["release_date"]
							epoch = calendar.timegm(convertToDateTime(release).timetuple())
							timeResults[str(epoch)]=int(score)
							gameResults.append(data["results"][i])

			else:
				mcResponse = unirest.post("https://byroredux-metacritic.p.mashape.com/search/game",
				  headers={
				    "X-Mashape-Key": "EH1nc2m4yDmshwgsHTweFUIFxXaJp1eJsYgjsnfs4eKkDP7LQy",
				    "Content-Type": "application/x-www-form-urlencoded"
				  },
				  params={
				    "max_pages": 1,
				    "retry": 4,
				    "title": data["results"][i]["name"]
				  }
				)
				#print platform
				#print data["results"][i]["name"]
				if(mcResponse.body['count']!=0):
						score= mcResponse.body["results"][0]["score"]
						data["results"][i]["score"] = score
						#print data["results"][i]["release_date"][5:7]
						data["results"][i]["release_month"] = monthStr(data["results"][i]["release_date"][5:7])
						data["results"][i]["name"] = gameName
						data["results"][i]["url"] = data["results"][i]["site_detail_url"]

						#print data["results"][i]
						if(score!="" and (gameName not in uniqueGameNames)):
							release = data["results"][i]["release_date"]
							epoch = calendar.timegm(convertToDateTime(release).timetuple())
							timeResults[str(epoch)]=int(score)
							timeResults[str(calendar.timegm(convertToDateTime(data["results"][i]["release_date"]).timetuple()))] = score
							gameResults.append(data["results"][i])
						#otherwise, don't log it into the database, it is scoreless
				
				
		i=i+1
		uniqueGameNames.add(gameName)


	offset+=100
json.dump(gameResults, f)
json.dump(timeResults, f2)
f.close()
f2.close()


#print platformSet
