####################################### This code is Written and documented by Subas Gupta ##################################################################


#########################################################  Start #######################################################################################

# Importing the required Libraries
from pymongo import MongoClient
import requests
import json
from datetime import datetime
import pandas as pd
import re

# these data we will get from somewhere
username = 'subasgupta9'
password = 'Subas@1997'
CompaignID = ''
postUrl = "https://www.instagram.com/p/CThKpxWI4Nz/"

# Instagram login url
link = 'https://www.instagram.com/accounts/login/'
login_url = 'https://www.instagram.com/accounts/login/ajax/'

# session Strating
session = requests.Session()
time = int(datetime.now().timestamp())
response = session.get(link)
csrf = response.cookies['csrftoken']

# payload for login
payload = {
    'username': username,
    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
    'queryParams': {},
    'optIntoOneTap': 'false'
}


# header for login
login_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/accounts/login/",
    "x-csrftoken": csrf
}

# Request to instagram for login
login_response = session.post(login_url, data=payload, headers=login_header)
login_data = json.loads(login_response.text)

# checking whether login is successful or failed
if(login_data["authenticated"]):
    print("Connection Successful")

else:
    print("login failed", login_response.text)


# Extracting the sessionId from cookies
cookies = login_response.cookies
cookies = cookies.get_dict()
sessionid = cookies['sessionid']
##################################################################### Likers Extraction ##########################################################


####################################### Running PhantomBuster Liker Agent ####################################

headers = {
    'Content-Type': 'application/json',
    'x-phantombuster-key': 'pPE4n2Gmzc5tubiUYCbyQoNJih9SlyLlGcNncX4Hcqs',
}

data = {"id": "8135696277865416", "argument": {"sessionCookie": sessionid,
                                               "spreadsheetUrl": postUrl, "columnName": "", "numberOfPhotosPerLaunch": 1}}
data = json.dumps(data)

response = requests.post(
    'https://api.phantombuster.com/api/v2/agents/launch', headers=headers, data=data)


####################################### Extracting ContainerID for Liker agent Output ############################

url = "https://api.phantombuster.com/api/v1/agent/8135696277865416/output"

headers = {
    "Accept": "application/json",
    "X-Phantombuster-Key-1": "pPE4n2Gmzc5tubiUYCbyQoNJih9SlyLlGcNncX4Hcqs"
}

response = requests.request("GET", url, headers=headers).json()
containerId = int(response['data']['containerId'])

####################################### Extracting url using containerId where results is hosted ######################


url = "https://api.phantombuster.com/api/v2/containers/fetch-output?id={0}".format(
    containerId)
headers = {
    "Accept": "application/json",
    "X-Phantombuster-Key": "pPE4n2Gmzc5tubiUYCbyQoNJih9SlyLlGcNncX4Hcqs"
}

response = requests.request("GET", url, headers=headers)
data = response.json()
r = json.dumps(data)
urls = re.findall(
    '(https:\/\/phantombuster\.s3\.amazonaws\.com\/[a-zA-Z0-9]+\/[a-zA-Z0-9]+.[a-z]+.json)', r)
url = ''
for link in urls:
    url = link


#################################### Loading hosted json data into pandas dataframe  ##################################

jsonData = pd.read_json(url)
usersData = pd.DataFrame(jsonData)
usersData.rename(columns={'photoUrl': 'postId'}, inplace=True)

################################## Extracting username from dataframe and scrapping user facebook id  ######################
"""
username = usersData['username']
usersData['fbid'] = 123   ### dumy data it will update after extracting user fbid 
case_list = []
count = temp = 10000
for i in range(len(username)):
    # if(count == 10050):
    #   break
    url = f"https://www.instagram.com/{username[i]}/?__a=1"
    if(count % 5 == 0):
        temp += 1
    proxy = f"http://user-testOvonts-sessionduration-1:test123@in.smartproxy.com:{temp}"
    userTextData = requests.get(
        url, proxies={'http': proxy, 'https': proxy}).text
    userJsonData = json.loads(userTextData)
    usersData['fbid'][i] = userJsonData['graphql']['user']['fbid']
    count += 1
"""
##################################### Extracting PostId from PostURL and saving into postId column of dataframe  #######


for i in range(len(usersData['postId'])):
    temp = usersData['postId'][i]
    url = re.findall(r"\/p\/.{11}\/", temp)
    postId = ''
    for url in url:
        postId = url
        postId = postId[3:14]
    usersData['postId'][i] = postId

#####################################  Converting Dataframe to dictionary ################################################

data1 = usersData[['username', 'instagramID', 'postId']]
#data1 = usersData[['username,'fbid','instagramID','postId']]  ### if user fbid is scrapped from instagram
likers_data = data1.to_dict(orient='records')


####################################    Saving these records into mongodb databae #######################################
conn = MongoClient(
    "mongodb+srv://ovontsdev:nx7LgnXLduzKu5A@ovonts0.5ymhm.mongodb.net/development")
db = conn[CompaignID]
compaignId_Likers = str(CompaignID) + "_" + 'likers'
likerCollection = db[compaignId_Likers]
likerCollection.insert_many(likers_data)


############################################################ Commentors Extraction  ##############################################################

######################################### Running Commentors Phantom buster Agent ############################################################


headers = {
    'Content-Type': 'application/json',
    'x-phantombuster-key': 'pPE4n2Gmzc5tubiUYCbyQoNJih9SlyLlGcNncX4Hcqs',
}

data = {"id": "636628553468555", "argument": {"sessionCookie": sessionid,
                                              "spreadsheetUrl": postUrl, "columnName": "", "numberOfPhotosPerLaunch": 1}}
data = json.dumps(data)

response = requests.post(
    'https://api.phantombuster.com/api/v2/agents/launch', headers=headers, data=data)


####################################### Extracting ContainerID for Liker agent Output ############################

url = "https://api.phantombuster.com/api/v1/agent/636628553468555/output"

headers = {
    "Accept": "application/json",
    "X-Phantombuster-Key-1": "pPE4n2Gmzc5tubiUYCbyQoNJih9SlyLlGcNncX4Hcqs"
}

response = requests.request("GET", url, headers=headers).json()
containerId = int(response['data']['containerId'])

####################################### Extracting url using containerId where results is hosted ######################

url = "https://api.phantombuster.com/api/v2/containers/fetch-output?id={0}".format(
    containerId)
headers = {
    "Accept": "application/json",
    "X-Phantombuster-Key": "pPE4n2Gmzc5tubiUYCbyQoNJih9SlyLlGcNncX4Hcqs"
}

response = requests.request("GET", url, headers=headers)
data = response.json()
r = json.dumps(data)
urls = re.findall(
    '(https:\/\/phantombuster\.s3\.amazonaws\.com\/[a-zA-Z0-9]+\/[a-zA-Z0-9]+.[a-z]+.json)', r)
url = ''
for link in urls:
    url = link

#################################### Loading hosted json data into pandas dataframe  ##################################

jsonData = pd.read_json(url)
usersData = pd.DataFrame(jsonData)
usersData = usersData[['username', 'ownerId', 'query']]
usersData.rename(columns={'ownerId': 'instagramID',
                 'query': 'postId'}, inplace=True)

################################## Extracting username from dataframe and scrapping user facebook id  ######################
"""
username = usersData['username']
usersData['fbid'] = 123   ###  fbid column filling with dumy data and it will update after extracting user fbid
case_list = []
count = temp = 10000
for i in range(len(username)):
    # if(count == 10050):
    #   break
    url = f"https://www.instagram.com/{username[i]}/?__a=1"
    if(count % 5 == 0):
        temp += 1
    proxy = f"http://user-testOvonts-sessionduration-1:test123@in.smartproxy.com:{temp}"
    userTextData = requests.get(
        url, proxies={'http': proxy, 'https': proxy}).text
    userJsonData = json.loads(userTextData)
    usersData['fbid'][i] = userJsonData['graphql']['user']['fbid']
    count += 1
"""

##################################### Extracting PostId from PostURL and saving into postId column of dataframe  #######

for i in range(len(usersData['postId'])):
    temp = usersData['postId'][i]
    url = re.findall(r"\/p\/.{11}\/", temp)
    postId = ''
    for url in url:
        postId = url
        postId = postId[3:14]
    usersData['postId'][i] = postId

#####################################  Converting Dataframe to dictionary ################################################

data1 = usersData[['username', 'instagramID', 'postId']]
#data1 = usersData[['username,'fbid','instagramID','postId']]   ### if user fbid is scrapped from instagram
commentors_data = data1.to_dict(orient='records')

####################################    Saving these records into mongodb databae #######################################
conn = MongoClient(
    "mongodb+srv://ovontsdev:nx7LgnXLduzKu5A@ovonts0.5ymhm.mongodb.net/development")
db = conn[CompaignID]
compaignId_Commentors = str(CompaignID) + "_" + 'commentors'
commentorsCollection = db[compaignId_Commentors]
commentorsCollection.insert_many(commentors_data)


###################################################################### End ###############################################################################
