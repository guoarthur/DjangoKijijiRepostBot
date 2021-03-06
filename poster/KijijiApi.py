import requests
import json
import bs4
import re
import sys
from multiprocessing import Pool

if sys.version_info < (3, 0):
    raise Exception("This program requires Python 3.0 or greater")

class KijijiApiException(Exception):
    def __init__(self, dump=None):

        if dump:
            pass
            #print(dump)
            #with open('/tmp/kijiji-api-dump', 'w') as dumpfile:
            #    dumpfile.write(dump)
    def __str(self):
        return 'View /tmp/kijiji-api-dump/ for last dumpfile'

class SignInException(KijijiApiException):
    def __str__(self):
        return 'Could not sign in.\n'+super().__str__()

class PostAdException(KijijiApiException):
    def __str__(self):
        return 'Could not post ad.\n'+super().__str__()

class DeleteAdException(KijijiApiException):
    def __str__(self):
        return 'Could not delete ad.\n'+super().__str__()


#Retrive CSRF token from webpage
#Tokens are different every time a page is visitied. 
def getToken(html, tokenName):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    res = soup.select('[name='+tokenName+']')[0]
    return res['value']

def uploadOneImage(imgFile):
    #Try three times to upload the file. If successful, return the url.
    imageUploadUrl = 'https://www.kijiji.ca/p-upload-image.html'
    for i in range (0, 3):
        files = {'file': imgFile}
        ses = requests.Session()
        r = ses.post(imageUploadUrl, files = files)
        if (r.status_code != 200):
            raise PostAdException(r.text)
        try:
            imageTree = json.loads(r.text)
            imgUrl = imageTree['thumbnailUrl']
            print("Image Upload success")
            return imgUrl
        except KeyError as e:
            print("Image Upload failed")
            pass
    return;



class KijijiApi:
    #login:  user, password -> None (Sets session to logged in)
    #isLoggedIn: None -> bool
    #All function requires a logged in session to function correctly
    #logout: None -> None
    #postAd: PostingFile -> adId
    #deleteAd: adId -> None
    #deleteAdUsingTitle: adTitle -> None
    #getAllAds: None -> list(vector(adname, adId))

    def __init__(self):
        config = {}
        self.session = requests.Session()

    def login(self, username, password):
        url = 'http://www.kijiji.ca/h-kitchener-waterloo/1700212'
        resp = self.session.get(url)

        url = 'https://www.kijiji.ca/t-login.html'
        resp = self.session.get(url)

        payload = {'emailOrNickname': username,
                'password': password,
                'rememberMe': 'true',
                '_rememberMe': 'on',
                'ca.kijiji.xsrf.token': getToken(resp.text, 'ca.kijiji.xsrf.token'),
                'targetUrl': 'L3QtbG9naW4uaHRtbD90YXJnZXRVcmw9TDNRdGJHOW5hVzR1YUhSdGJEOTBZWEpuWlhSVmNtdzlUREpuZEZwWFVuUmlNalV3WWpJMGRGbFlTbXhaVXpoNFRucEJkMDFxUVhsWWJVMTZZbFZLU1dGVmJHdGtiVTVzVlcxa1VWSkZPV0ZVUmtWNlUyMWpPVkJSTFMxZVRITTBVMk5wVW5wbVRHRlFRVUZwTDNKSGNtVk9kejA5XnpvMnFzNmc2NWZlOWF1T1BKMmRybEE9PQ--'
                }
        resp = self.session.post(url, data = payload)
        if not self.isLoggedIn():
            raise SignInException(resp.text)

    def isLoggedIn(self):
        indexPageText = self.session.get('https://www.kijiji.ca/m-my-ads.html/').text
        return 'Sign Out' in indexPageText 

    def logout(self):
        resp = self.session.get('https://www.kijiji.ca/m-logout.html')

    def deleteAd(self, adId):
        myAdsPage = self.session.get('https://www.kijiji.ca/m-my-ads.html')

        params = {'Action': 'DELETE_ADS',
                'Mode': 'ACTIVE',
                'needsRedirect': 'false',
                'ads': '[{{"adId":"{}","reason":"PREFER_NOT_TO_SAY","otherReason":""}}]'.format(str(adId)),
                'ca.kijiji.xsrf.token': getToken(myAdsPage.text, 'ca.kijiji.xsrf.token')
                }
        resp = self.session.post('https://www.kijiji.ca/j-delete-ad.json', data = params)
        if ("OK" not in resp.text):
            raise DeleteAdException(resp.text)

    def deleteAdUsingTitle(self, title):
        allAds = self.getAllAds()
        [self.deleteAd(i) for t, i in allAds if t.strip() == title.strip()]
        
    #Allow user to pass in photos (as a array of string) they want to upload
    #Upload images concurrently using Pool
    def uploadImage(self, imageFiles=[]):
        images = []

        imageUploadUrl = 'https://www.kijiji.ca/p-upload-image.html'
        for image in imageFiles:
            images.append(uploadOneImage(image))
        """
        with Pool(5) as p:
            images = p.map(uploadOneImage, imageFiles)
        """
        return [image for image in images if image is not None]
    
    #Data is a Dictionary that represents the data that will be posted to Kijijiserver
    #imageFiles represents a bunch of opened files (in string format) that need to be uploaded 
    def postAdUsingData(self, data, imageFiles=[]):
        #Upload the images
        imageList = self.uploadImage(imageFiles)
        data['images'] = ",".join(imageList)
        
        #Load ad posting page
        resp = self.session.get('https://www.kijiji.ca/p-admarkt-post-ad.html?categoryId=772')
        
        #Retrive tokens for website
        xsrfToken = getToken(resp.text, 'ca.kijiji.xsrf.token') 
        fraudToken = getToken(resp.text, 'postAdForm.fraudToken')
        data['ca.kijiji.xsrf.token']=xsrfToken
        data['postAdForm.fraudToken']=fraudToken

        #Upload the ad itself
        newAdUrl="https://www.kijiji.ca/p-submit-ad.html"
        resp = self.session.post(newAdUrl, data=data)
        if (resp.status_code != 200 or \
                "message-container success" not in resp.text):
            raise PostAdException(resp.text)

        #Get adId and return it
        newCookieWithAdId = resp.headers['Set-Cookie']
        adId = re.search('\d+', newCookieWithAdId).group()
        return adId

    def getAllAds(self):
        myAdsUrl = 'http://www.kijiji.ca/j-get-my-ads.json'
        myAdsPage = self.session.get(myAdsUrl)
        myAdsTree = json.loads(myAdsPage.text) 
        adIds = [entry['id'] for entry in myAdsTree['myAdEntries']]
        adNames = [entry['title'] for entry in myAdsTree['myAdEntries']]
        return zip(adNames, adIds)

