import requests
from constants import HOMEASSISTANT_URL

class HomeAssistantClient:
    def __init__(self, token):
        self.client = requests.session()
        self.client.headers.update({'Authorization': 'Bearer ' + token})
        self.client.headers.update({'Content-Type': 'application/json'})
        self.client.headers.update({'Accept': 'application/json'})
        self.client_url = HOMEASSISTANT_URL + "/api/"

    def _make_request(self, endpoint, method='post', data=None):
        url = self.client_url + endpoint
        if method.lower() == 'post':
            response = self.client.post(url, json=data)
        elif method.lower() == 'get':
            response = self.client.get(url)
        else:
            raise ValueError("Invalid HTTP method")

       
        json_response = response.json()
        return json_response

    def toggle(self, entity_id):
        data = {"entity_id": entity_id}
        self._make_request("services/homeassistant/toggle", data=data)

    def turn_on(self, entity_id):
        data = {"entity_id": entity_id}
        self._make_request("services/homeassistant/turn_on", data=data)

    def turn_off(self, entity_id):
        data = {"entity_id": entity_id}
        self._make_request("services/homeassistant/turn_off", data=data)

    def get_state(self, entity_id):
        return self._make_request("states/" + entity_id, method='get')
    
    def get_states(self):
        return self._make_request("states", method='get')
    
    def find_entity_id(self, device_class):
        states = self.get_states()
        # find smart plug
        smart_plug_id = None
        for state in states:
            if not 'device_class' in state['attributes']:
                continue

            if state['attributes']['device_class'] == device_class:
                smart_plug_id = state['entity_id']
                break
        return smart_plug_id
