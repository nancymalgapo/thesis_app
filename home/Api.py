import requests
import time

client_id = "103369"
client_secret = "O92K5e5Ar6zWVamBoTjEyeUavrODqvk5"
mode = 1

class PlagScan():

    def get_access_token(self):
        url = "https://api.plagscan.com/v3/token"

        data = {}
        data['client_id'] = client_id
        data['client_secret'] = client_secret
        response = requests.post(url, json=data)
        json = response.json()
        #response_data = json['data']
        return json['access_token']

    def document_submit(self, file_location, newdoc):
        access_token = self.get_access_token()
        url = "https://api.plagscan.com/v3/documents?access_token={}".format(access_token)

        #headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {'fileUpload':open('media/'+ str(file_location), 'rb')}
        files = {'fileUpload':open('media/' + str(file_location), 'rb') }
        response = requests.post(url, data=data, files=files)
        json = response.json()
        response_data = json['data']
        docID = response_data['docID']
        newdoc.docID = docID
        newdoc.save()
        #time.sleep(5)
        return docID

    def document_check_plagiarism(self, docID):
        access_token = self.get_access_token()
        url = "https://api.plagscan.com/v3/documents/{}/check?access_token={}".format(docID, access_token)
        data = {"docID":docID}
        response = requests.put(url, data)
        try:
            json = response.json()
        except ValueError:
            # return("Document has start to be analyzed for plagiarism")
            return "checking"
        print (json)
        response_data = json['error']
        message = response_data['message']
        print (message)
        return message

    def document_analyzed_status(self, docID):
        access_token = self.get_access_token()
        url = "https://api.plagscan.com/v3/documents/{}?access_token={}".format(docID, access_token)
        response = requests.get(url,)
        if ('error' in response.json()):
            return "converting"
        response_data = response.json()['data']
        state = response_data['state']
        if state == "3":
            return "done"
        elif state == "0": 
            return "not"
        elif state == "1" or state == "2":
            return "checking"

    def document_report(self, docID):
        access_token = self.get_access_token()
        url = "https://api.plagscan.com/v3/documents/{}/retrieve?access_token={}&mode={}".format(docID, access_token, mode)
        response = requests.get(url,)
        response_data = response.json()['data']
        return response_data