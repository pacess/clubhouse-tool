##----------------------------------------------------------------------------------------
##  Clubhouse Room Profile Picture Downloader
##----------------------------------------------------------------------------------------
##  Platform: Raspberry Pi 4 + Ubuntu 20 + Python 3.8.5 + mitmproxy 4.0.4
##  Written by Pacess HO
##  Copyrights Pacess Studio, 2021.  All rights reserved.
##----------------------------------------------------------------------------------------

##  mitmdump -v --ignore-hosts ^www\.clubhouseapi\.com:443$ -s clubhouse_profile_downlader.py

##  Profile picture
##  https://clubhouseprod.s3.amazonaws.com/5161304_f249cde4-d24b-4d59-925b-b4931203218e
##  https://clubhouseprod.s3.amazonaws.com:443/2080885366_e984b3ae-26b4-4995-9bb0-1b0ba8047890_thumbnail_250x250

from datetime import datetime
import urllib.request
import json
import os

##----------------------------------------------------------------------------------------
##  Global variables
rootFolder = "__json__/"
fileIndex = 0

for currentFolder, directoryArray, fileArray in os.walk(rootFolder):
	for filename in fileArray:
		
		if (filename.startswith(".")):
			continue
		
		jsonPath = os.path.join(currentFolder, filename)
		print("Reading: "+jsonPath)
		with open(jsonPath) as file:
			
			##  Audience list JSON
			jsonContent = file.read()
			
			##  Extract JSON
			jsonDictionary = json.loads(jsonContent)
			
			if ("m" not in jsonDictionary):
				continue
			
			memberArray = jsonDictionary["m"]
			for member in memberArray: 
				
				##  Member
				##	"d": {
				##		"action": "join_channel",
				##		"channel": "PrnOkN9j",
				## 		"user_profile": {
				## 			"user_id": 2080885366,
				## 			"name": "Vian Fung",
				## 			"photo_url": "https://clubhouseprod.s3.amazonaws.com:443/2080885366_e984b3ae-26b4-4995-9bb0-1b0ba8047890_thumbnail_250x250",
				## 			"username": "vianvian",
				## 			"first_name": "Vian",
				## 			"skintone": 3,
				## 			"is_new": true,
				## 			"is_speaker": false,
				## 			"is_moderator": false,
				## 			"time_joined_as_speaker": null,
				## 			"is_followed_by_speaker": true,
				## 			"is_invited_as_speaker": false
				##  	}
				## 	}
				dataDictionary = member["d"]

				## 	"action": "join_channel",
				## 	"action": "leave_channel",
				if ("user_profile" not in dataDictionary):
					continue

				profile = dataDictionary["user_profile"]
				
				if ("photo_url" not in profile):
					continue
				
				photoURL = profile["photo_url"]
				if (not photoURL):
					continue
				
				largePhotoURL = photoURL.replace("_thumbnail_250x250", "")
				
				if ("user_id" not in profile):
					continue
				if ("username" not in profile):
					continue
				
				userID = profile["user_id"]
				username = profile["username"]
				
				##  Download photo
				filename = largePhotoURL.rsplit("/", 1)[-1]
				folder = "__profile__/"+str(userID)[-2:]
				filePath = folder+"/"+filename+"_"+username+".jpg"

				if not os.path.exists(folder):
					os.makedirs(folder)
				
				if os.path.exists(filePath):
					continue

				try:
					print("- Downloading "+largePhotoURL)
					urllib.request.urlretrieve(largePhotoURL, filePath)
				except urllib.error.HTTPError as e:
					print("  ### "+str(e))
