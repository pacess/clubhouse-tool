##----------------------------------------------------------------------------------------
##  MITMProxy Clubhouse Room Action Recorder
##----------------------------------------------------------------------------------------
##  Platform: Raspberry Pi 4 + Ubuntu 20 + Python 3.8.5 + mitmproxy 4.0.4
##  Written by Pacess HO
##  Copyrights Pacess Studio, 2021.  All rights reserved.
##----------------------------------------------------------------------------------------

##  mitmdump -v --ignore-hosts ^www\.clubhouseapi\.com:443$ -s mitmproxy_clubhouse_room_recorder.py

##  Status update URL
##  https://clubhouse.pubnub.com/v2/subscribe/sub-c-a4abea84-9ca3-11ea-8e71-f2b83ac9263d/channel_all.Mdj6bQZo,users.4396277,channel_user.Mdj6bQZo.4396277/0?instanceid=7818808C-2A64-434E-B6ED-143C432DE849&deviceid=2490496E-5575-4E0E-91E9-03793D54846C&uuid=4396277&pnsdk=PubNFub-ObjC-iOS%2F4.15.7&requestid=10295840-3187-4EEA-8F0A-2A784FF41055&auth=96f8b544-e152-42c4-ba8d-4b6cfd2c99cf&tt=16128706748752437&heartbeat=60&tr=4

from datetime import datetime
from mitmproxy import http
import os
import re

##----------------------------------------------------------------------------------------
##  Global variables
_today = datetime.today().strftime("%Y%m%d")
_fileIndexDictionary = {}
_roomID = ""

##----------------------------------------------------------------------------------------
def response(flow: http.HTTPFlow):
	global _fileIndexDictionary
	global _roomID
	global _today
	
	##  Audience list domain
	if (flow.request.pretty_host == "clubhouse.pubnubapi.com"):
		if (flow.request.path.startswith("/v2/subscribe")):
			
			##  Extract room ID from URL
			_roomIDArray = re.findall('channel_user\.(.*?)\..*', flow.request.path)

			if (len(_roomIDArray) == 0):
				return
				
			_roomID = _roomIDArray[0]
			
			##  Update counter
			if (_roomID in _fileIndexDictionary):
				_fileIndexDictionary[_roomID] = _fileIndexDictionary[_roomID]+1
			else:
				_fileIndexDictionary[_roomID] = 1
				_today = datetime.today().strftime("%Y%m%d")
			
			##  Subfolder name
			subfolderID = int(_fileIndexDictionary[_roomID]/1000)
			subfolder = str(subfolderID).zfill(4)+"/"
			
			folder = "/var/www/www.pacess.com/storage/app/clubhouse-statistics/json/"+_today+"/"+_roomID+"/"
			
			filenameID = str(_fileIndexDictionary[_roomID]).zfill(4)
			filename = _roomID+"_"+filenameID+".json"
			
			##  Create folder if not exists
			if not os.path.exists(folder+subfolder):
				os.makedirs(folder+subfolder)
			
			##  Save JSON to file
			filePath = folder+subfolder+filename
			with open(filePath, "wb") as f:
				f.write(flow.response.content)
				f.close()
			
			print("   JSON saved: "+filePath)
