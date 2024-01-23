import requests
from typing import Tuple, List
from constants import HOMEASSISTANT_URL
from homeassistant.Models.Switch import Switch
from homeassistant.Models.Media_Player import Media_Player
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

        try:
            json_response = response.json()
            return json_response
        except:
            raise ValueError("Invalid response: " + str(response.content))
    
    def health_check(self):
        try:
            data = self._make_request("", method='get')
            return data['message'] == 'API running.'
        except:
            return False

    def set_state(self, entity_id, action, data={}):
        domain, _ = entity_id.split('.')
        actions = self.get_possible_actions(entity_id)
        actions_names = [action['action'] for action in actions]
        if action not in actions_names:
            raise ValueError("Invalid action, valid actions are: " + str(actions_names))
        
        data = {"entity_id": entity_id, **data}
        self._make_request("services/" + domain + "/" + action, data=data)
        
        
    def get_possible_actions(self, entity_id):
        id_type, _ = entity_id.split('.')
        services = self._make_request("services", method='get')
        actions = []
        for service in services:
            if service['domain'] == id_type:
                actions = []
                for action, action_data in service['services'].items():
                    # deconstruct action_data
                    actions.append({ 'action': action, **action_data })
                
        return actions


    def get_state(self, entity_id):
        return self._make_request("states/" + entity_id, method='get')
    
    
    def get_states(self):
        return self._make_request("states", method='get')
    
    
    def find_switches(self) -> List[Switch]:
        states = self.get_states()
        switches: List[Switch] = []
        for state in states:
            if state['entity_id'].startswith('switch.'):
                switches.append(Switch(state['entity_id'], self))
        return switches
    
    
    def find_media_players(self) -> List[Media_Player]:
        states = self.get_states()
        media_players: List[Media_Player] = []
        for state in states:
            if state['entity_id'].startswith('media_player.'):
                media_players.append(Media_Player(state['entity_id'], self))
        return media_players
          
    
    def find_entity_by_attributes(self):
        # TODO Add Lights
        print("Hello")
        states = self.get_states()
         
        switches: List[Switch] = []
        media_players: List[Media_Player] = []
        
        for state in states:
            if state['entity_id'].startswith('switch.'):
                switches.append(Switch(state['entity_id'], self))
            elif state['entity_id'].startswith('media_player.'):
                media_players.append(Media_Player(state['entity_id'], self))
        
        return {
            'switches': switches,
            'media_players': media_players
        }

    def find_entity_by_id(self, id):
        states = self.get_states()
        for state in states:
            if state['entity_id'] == id:
                if state['entity_id'].startswith('switch.'):
                    return Switch(state['entity_id'], self)
                elif state['entity_id'].startswith('media_player.'):
                    return Media_Player(state['entity_id'], self)
        return None

