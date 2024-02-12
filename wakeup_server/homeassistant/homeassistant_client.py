import requests
from typing import Tuple, List
from constants import HOMEASSISTANT_URL
from homeassistant.Models.Switch import Switch
from homeassistant.Models.Media_Player import Media_Player
from requests.exceptions import ConnectionError
import datetime
import json

class HomeAssistantClient:
    def __init__(self, token):
        self.client = requests.session()
        self.client.headers.update({'Authorization': 'Bearer ' + token})
        self.client.headers.update({'Content-Type': 'application/json'})
        self.client.headers.update({'Accept': 'application/json'})
        self.client_url = HOMEASSISTANT_URL + "/api/"


    def _make_request(self, endpoint, method='post', data=None):
        url = self.client_url + endpoint
        
        try:
            response = None
            if method.lower() == 'post':
                response = self.client.post(url, json=data)
            elif method.lower() == 'get':
                response = self.client.get(url)
            else:
                raise ValueError("Invalid HTTP method")
              
            if response is None or response.status_code != 200:
                print(response)
                error_message = "Invalid response: " + str(response.content) if response is not None else "No response"
                raise ValueError("Invalid response: " + error_message)  
            
            json_response = response.json()
            return json_response
        except ConnectionError as e:
            raise ConnectionError("Connection error: " + str(e))
        except Exception as e:
            raise ValueError("Error: " + str(e))
    
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

    def getLogsPerEntity(self, entity_id):
        today_date = datetime.date.today()
        yesterday_date = today_date - datetime.timedelta(days=1)
        today_date_complete = str(today_date) + "T12:00:00.000000"  #should be T00:00:00.000000 if midnight is the retrieval time
        yesterday_date_complete = str(yesterday_date) + "T12:00:00.000000" #should be T00:00:00.000000 
        request_string = "history/period/" + yesterday_date_complete + "?filter_entity_id=" + str(entity_id) + "&end_time=" + today_date_complete
        data = self._make_request(request_string, method='get')
        day_usage_data = data[0]

        number_of_toggles = 0
        for entry in day_usage_data:
            if(entry['state'] != "unavailable"):
                number_of_toggles += 1
        print("Number of toggles:", number_of_toggles)

        total_on_time = []
        start_time = None
        end_time = None
        first_iteration = True
        for entry in day_usage_data:
            if(entry['state'] == "on"):
                start_time = entry['last_changed']
                if first_iteration:
                    on_time = datetime.datetime.fromisoformat(start_time) - datetime.datetime.fromisoformat(yesterday_date_complete + "+00:00")
                    total_on_time.append(on_time)
            if(entry['state'] != "on" and start_time != None):
                end_time = entry['last_changed']
                on_time = datetime.datetime.fromisoformat(end_time) - datetime.datetime.fromisoformat(start_time)
                total_on_time.append(on_time)
                start_time = None
                end_time = None
            first_iteration = False
        if(start_time != None):
            on_time = datetime.datetime.fromisoformat(today_date_complete + "+00:00") - datetime.datetime.fromisoformat(start_time)
            total_on_time.append(on_time)
        total_on_time_result = total_on_time[0]
        for i in range(1, len(total_on_time)):
            total_on_time_result += total_on_time[i]
        print("Total on time:" , total_on_time_result)
        
        total_off_time = []
        start_time = None
        end_time = None
        first_iteration = True
        for entry in day_usage_data:
            if(entry['state'] == "off"):
                start_time = entry['last_changed']
                if first_iteration:
                    off_time = datetime.datetime.fromisoformat(start_time) - datetime.datetime.fromisoformat(yesterday_date_complete + "+00:00")
                    total_off_time.append(off_time)
            if(entry['state'] != "off" and start_time != None):
                end_time = entry['last_changed']
                off_time = datetime.datetime.fromisoformat(end_time) - datetime.datetime.fromisoformat(start_time)
                total_off_time.append(off_time)
                start_time = None
                end_time = None
            first_iteration = False
        if(start_time != None):
            off_time = datetime.datetime.fromisoformat(today_date_complete + "+00:00") - datetime.datetime.fromisoformat(start_time)
            total_off_time.append(off_time)
        total_off_time_result = total_off_time[0]
        for i in range(1, len(total_off_time)):
            total_off_time_result += total_off_time[i]
        print("Total off time:" , total_off_time_result)

        total_unavailable_time = []
        start_time = None
        end_time = None
        first_iteration = True
        for entry in day_usage_data:
            if(entry['state'] == "unavailable"):
                start_time = entry['last_changed']
                if first_iteration:
                    unavailable_time = datetime.datetime.fromisoformat(start_time) - datetime.datetime.fromisoformat(yesterday_date_complete + "+00:00")
                    total_unavailable_time.append(unavailable_time)
            if(entry['state'] != "unavailable" and start_time != None):
                end_time = entry['last_changed']
                unavailable_time = datetime.datetime.fromisoformat(end_time) - datetime.datetime.fromisoformat(start_time)
                total_unavailable_time.append(unavailable_time)
                start_time = None
                end_time = None
            first_iteration = False
        if(start_time != None):
            unavailable_time = datetime.datetime.fromisoformat(today_date_complete + "+00:00") - datetime.datetime.fromisoformat(start_time)
            total_unavailable_time.append(unavailable_time)
        total_unavailable_time_result = total_unavailable_time[0]
        for i in range(1, len(total_unavailable_time)):
            total_unavailable_time_result += total_unavailable_time[i]
        print("Total unavailable time:" , total_unavailable_time_result)

        return today_date_complete, number_of_toggles, total_on_time_result, total_off_time_result, total_unavailable_time_result






