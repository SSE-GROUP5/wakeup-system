import requests
import json

class PatientInfoFetch:
    def __init__(self, serverURL):
        self.serverURL = serverURL


    def nameFetch(self, ID : str):
        url = self.serverURL + ID
        response = requests.get(url)

        if response.status_code == 200:
            patient = json.loads(response.text)
            print(patient['name'][0]['family'])
            print(patient['name'][0]['given'])

            familyName = patient['name'][0]['family']
            givenName = ' '.join([gName + " " for gName in patient['name'][0]['given']])

            return givenName + familyName
        else:
            print(f"Error fetching data: {response.status_code}")



if __name__ == "__main__":
    infoFetch = PatientInfoFetch('https://hapi.fhir.org/baseR4/Patient/')
    print(infoFetch.nameFetch('593047'))




