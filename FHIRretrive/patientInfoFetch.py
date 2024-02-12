import requests
import json




def nameFetch(serverURL, ID : str):
    url = serverURL + ID
    response = requests.get(url)

    if response.status_code == 200:
        patient = json.loads(response.text)
        print(patient['name'][0]['family'])
        print(patient['name'][0]['given'])

        familyName = patient['name'][0]['family']
        givenName = ' '.join([gName + " " for gName in patient['name'][0]['given']])

        return givenName.strip(), familyName.strip()
    else:
        print(f"Error fetching data: {response.status_code}")



if __name__ == "__main__":
    givenName,  familyName= nameFetch('https://hapi.fhir.org/baseR4/Patient/', '593047')
    print(givenName + " " + familyName)




