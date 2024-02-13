import requests
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from constants import FHIR_DB_URL


class DataFetchError(Exception):
    pass

def nameFetch(gosh_id : str):
    if not FHIR_DB_URL:
        raise ValueError('No FHIR URL, please set up in .env file')
    
    url = FHIR_DB_URL + gosh_id

    response = requests.get(url)

    if response.status_code == 200:
        patient = json.loads(response.text)
        print(patient['name'][0]['family'])
        print(patient['name'][0]['given'])

        familyName = patient['name'][0]['family']
        givenName = ' '.join([gName + " " for gName in patient['name'][0]['given']])

        return givenName.strip(), familyName.strip()
    elif response.status_code == 400:
        raise DataFetchError(f"Bad Request: The request was unacceptable, often due to missing a required parameter.")
    elif response.status_code == 401:
        raise DataFetchError(f"Unauthorized: No valid API key provided.")
    elif response.status_code == 403:
        raise DataFetchError(f"Forbidden: The API key doesn't have permissions to perform the request.")
    elif response.status_code == 404:
        raise DataFetchError(f"Not Found: The requested resource doesn't exist.")
    elif response.status_code == 500:
        raise DataFetchError(f"Internal Server Error: We had a problem with the server. Try again later.")
    else:
        raise DataFetchError(f"Error fetching data: {response.status_code}")



if __name__ == "__main__":
    givenName,  familyName= nameFetch('456')
    print(givenName + " " + familyName)




